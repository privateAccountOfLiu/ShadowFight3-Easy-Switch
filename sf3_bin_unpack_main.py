import csv
import numpy as np
from constant_values import *
import argparse


class Bone:
    def __init__(self, position: iter, rotation: iter, parent, bone_id: int, trs: int):
        self.pos, self.rot = position, rotation
        self.parent, self.id = parent, bone_id
        self.trs = trs
        self.name = bones_dict.get(self.id)
        self.local_met, self.global_met = self.transform()[0], self.transform()[1]

    def __str__(self):
        return bones_str.format(self.id, self.name, self.pos, self.rot,
                                self.parent.name if self.parent is not None else None, self.trs)

    def transform(self):
        m_local = np.vstack((np.hstack((self.rot, np.array([self.pos]).T)), np.array([[0, 0, 0, 1]])))
        if self.parent is None:
            return m_local, m_local
        else:
            m_global = np.dot(self.parent.global_met, m_local)
            return m_local, m_global

    def get_global_pos(self):
        return self.global_met[0: 3, 3]


def read_sf3_animation_binary(filename: str, is_old: bool) -> tuple[list[list[Bone]], list[int], list[int]]:
    with open(filename, 'rb') as f_bin:
        bin_str = f_bin.read()[26:]
        frames_num = unpack('I', pack('4B', *[i for i in bin_str[0:4]]))[0]
        bones_num = unpack('I', pack('4B', *[i for i in bin_str[4:8]]))[0]
        bones_index_o = [unpack('H',
                         pack('2B',
                              *[j for j in bin_str[8 + i * 2: 8 + i * 2 + 2]]))[0] for i in range(bones_num)]
        bones_index = sorted(bones_index_o)
    if is_old:
        data_out = unpack_for_old(bin_str, bones_num, frames_num, bones_index_o)
    else:
        data_out = unpack_for_new(bin_str, bones_num, frames_num, bones_index, bones_index_o)
    return data_out, bones_index_o, bones_index


def unpack_for_new(bin_str: bytes | int,
                   _bones_num: int,
                   _frames_num: int,
                   _bones_list: list[int],
                   _bones_list_o: list[int]) -> list[list[Bone]]:
    head_info_print(_frames_num, _bones_num, _bones_list_o,
                    8 + _bones_num * 2, 8 + _bones_num * 2 + _frames_num * _bones_num * 2 * 6)
    result, save_data, frame_data, f_index = [], [], [], 0
    for _i in range(8 + _bones_num * 2, 8 + _bones_num * 2 + _frames_num * _bones_num * 2 * 6 + 1, 12):
        data = [unpack_struct('2B',
                              form,
                              bin_str[_i + form_i * 2: _i + (form_i + 1) * 2]) for form_i, form in enumerate('eeeHHH')]
        q_0 = (((data[4] >> 14) + 4 * (data[3] & 8191)) * 2**0.5 / 32767) - 2**-0.5
        q_1 = (((data[5] >> 15) + 2 * (data[4] & 16383)) * 2**0.5 / 32767) - 2**-0.5
        q_2 = (((data[3] >> 16) + 1 * (data[5] & 32767)) * 2**0.5 / 32767) - 2**-0.5
        q_3 = (1 - (q_0**2 + q_1**2 + q_2**2))**0.5
        trans = (data[3] >> 13) & 3
        match trans:
            case 1:
                q_arr = (q_0, q_3, q_1, q_2)
            case 2:
                q_arr = (q_0, q_1, q_3, q_2)
            case 3:
                q_arr = (q_0, q_1, q_2, q_3)
            case _:
                q_arr = (q_3, q_0, q_1, q_2)
        q_x, q_y, q_z, q_w = q_arr
        met = np.array([[1-2*(q_y**2+q_z**2), 2*(q_x*q_y-q_w*q_z), 2*(q_x*q_z+q_w*q_y)],
                        [2*(q_x*q_y+q_w*q_z), 1-2*(q_x**2+q_z**2), 2*(q_y*q_z-q_w*q_x)],
                        [2*(q_x*q_z-q_w*q_y), 2*(q_y*q_z+q_w*q_x), 1-2*(q_x**2+q_y**2)]])
        if (_i - (8 + _bones_num*2)) % (_bones_num * 6 * 2) == 0 and _i != (8 + _bones_num*2):
            save_data.append(frame_data)
            frame_data = []
            f_index = 0
        get_parent_mes = parent_dict.get(_bones_list_o[f_index], -1)
        frame_data.append((data[0: 3], met, get_parent_mes, _bones_list_o[f_index], trans))
        f_index += 1
    for frame in save_data:
        frame.sort(key=lambda x: x[3])
        mid_saver = []
        for bone_iter, bone in enumerate(frame):
            if bone[2] != -1:
                mid_saver.append(Bone(bone[0], bone[1], mid_saver[_bones_list.index(bone[2])], bone[3], bone[4]))
            else:
                mid_saver.append(Bone(bone[0], bone[1], None, bone[3], bone[4]))
        result.append(mid_saver)
    return result


def unpack_for_old(bin_str: bytes | int, _bones_num: int, _frames_num: int, _bones_list: list[int]) -> list[list[Bone]]:
    head_info_print(_frames_num, _bones_num, _bones_list,
                    8 + _bones_num * 2, 8 + _bones_num * 2 + _frames_num * _bones_num * 4 * 7)
    result, frame_data, f_index = [], [], 0
    for _i in range(8 + _bones_num * 2, 8 + _bones_num * 2 + _frames_num * _bones_num * 4 * 7 + 1, 28):
        data = [unpack_struct('4B',
                              'f',
                              bin_str[_i + form_i * 4: _i + (form_i + 1) * 4]) for form_i in range(7)]
        q_x, q_y, q_z, q_w = data[3:]
        met = np.array([[1-2*(q_y**2+q_z**2), 2*(q_x*q_y-q_w*q_z), 2*(q_x*q_z+q_w*q_y)],
                        [2*(q_x*q_y+q_w*q_z), 1-2*(q_x**2+q_z**2), 2*(q_y*q_z-q_w*q_x)],
                        [2*(q_x*q_z-q_w*q_y), 2*(q_y*q_z+q_w*q_x), 1-2*(q_x**2+q_y**2)]])
        if (_i - (8 + _bones_num*2)) % (_bones_num * 7 * 4) == 0 and _i != (8 + _bones_num*2):
            result.append(frame_data)
            frame_data = []
            f_index = 0
        get_parent = frame_data[_bones_list.index(parent_dict.get(_bones_list[f_index]))] if frame_data else None
        frame_data.append(Bone(data[0: 3], met, get_parent, _bones_list[f_index], 3))
        f_index += 1
    return result


def data_to_csv(filename: str, _bones_list: list[int], _data: list[list[Bone]]) -> None:
    with open(filename, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        bones_name = [bones_dict.get(i, f'unknown{i}') for i in _bones_list]
        writer.writerow(bones_name)
        for i in _data:
            writer.writerow([j.get_global_pos().tolist() for j in i])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='target_file_path(string)', type=str)
    parser.add_argument('-o', '--isold', help='whether the quaternion compressed(bool)', type=bool)
    args = parser.parse_args()
    filepath, isold = args.filepath, args.isold
    if args.isold is None:
        isold = False
    animation, bones_index_list_o, bones_index_list = read_sf3_animation_binary(filepath, isold)
    fileout = 'out_animation.csv'
    data_to_csv(fileout, bones_index_list, animation)
