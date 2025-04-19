from struct import unpack, pack

lines = '''
l 2 1
l 3 2
l 4 3
l 5 4
l 6 5
l 7 3
l 8 7
l 9 8
l 10 9
l 11 10
l 12 10
l 13 12
l 14 12
l 15 14
l 16 15
l 17 12
l 18 17
l 19 18
l 20 12
l 21 20
l 22 21
l 23 8
l 24 7
l 25 3
l 26 25
l 27 26
l 28 27
l 29 28
l 30 28
l 31 30
l 32 30
l 33 32
l 34 33
l 35 30
l 36 35
l 37 36
l 38 30
l 39 38
l 40 39
l 41 26
l 42 25
l 43 1
l 44 43
l 45 44
l 46 45
l 47 46
l 48 43
l 49 1
l 50 49
l 51 50
l 52 51
l 53 52
l 54 49
l 55 9
l 56 27
l 57 44
l 58 50
'''

bones_str = 'id: {}\nname: {}\nposition: {}\nrotation: {}\nparent: {}\ntrans: {}\n'
bones_name_list_str = 'name of bones: {}'

bones_dict = {
    6: 'hair1',
    5: 'hair',
    4: 'head',
    3: 'neck',
    11: 'forearm_twist_l',
    13: 'weapon_l',
    16: 'f_big3_l',
    15: 'f_big2_l',
    14: 'f_big1_l',
    19: 'f_main3_l',
    18: 'f_main2_l',
    17: 'f_main1_l',
    22: 'f_pointer3_l',
    21: 'f_pointer2_l',
    20: 'f_pointer1_l',
    12: 'hand_l',
    10: 'forearm_l',
    9: 'arm_l',
    23: 'scapular_l',
    8: 'clavicle_l',
    24: 'chest_l',
    7: 'zero_joint_hand_l',
    29: 'forearm_twist_r',
    31: 'weapon_r',
    34: 'f_big3_r',
    33: 'f_big2_r',
    32: 'f_big1_r',
    37: 'f_main3_r',
    36: 'f_main2_r',
    35: 'f_main1_r',
    40: 'f_pointer3_r',
    39: 'f_pointer2_r',
    38: 'f_pointer1_r',
    30: 'hand_r',
    28: 'forearm_r',
    27: 'arm_r',
    41: 'scapular_r',
    26: 'clavicle_r',
    42: 'chest_r',
    25: 'zero_joint_hand_r',
    2: 'chest',
    1: 'stomach',
    47: 'toe_l',
    46: 'foot_l',
    45: 'calf_l',
    44: 'thigh_l',
    48: 'back_l',
    43: 'zero_joint_pelvis_l',
    55: 'toe_r',
    54: 'foot_r',
    53: 'calf_r',
    52: 'thigh_r',
    56: 'back_r',
    51: 'zero_joint_pelvis_r',
    57: 'biceps_twist_l',
    58: 'biceps_twist_r',
    59: 'thigh_twist_l',
    60: 'thigh_twist_r',
    0: 'pelvis'
}
parent_dict = {
    -1: None,
    1: 0,
    2: 1,
    25: 2,
    7: 2,
    3: 2,
    26: 25,
    42: 25,
    41: 26,
    27: 26,
    28: 27,
    58: 27,
    30: 28,
    29: 28,
    31: 30,
    38: 30,
    35: 30,
    32: 30,
    39: 38,
    40: 39,
    36: 35,
    37: 36,
    33: 32,
    34: 33,
    8: 7,
    24: 7,
    23: 8,
    9: 8,
    10: 9,
    57: 9,
    12: 10,
    11: 10,
    13: 12,
    20: 12,
    17: 12,
    14: 12,
    21: 20,
    22: 21,
    18: 17,
    19: 18,
    15: 14,
    16: 15,
    4: 3,
    5: 4,
    51: 0,
    52: 51,
    56: 51,
    60: 52,
    53: 52,
    54: 53,
    55: 54,
    43: 0,
    44: 43,
    48: 43,
    59: 44,
    45: 44,
    46: 45,
    47: 46
}


def head_info_print(_frames_num: int,
                    _bones_num: int,
                    _bones_list: list[int],
                    _animation_begin: int,
                    _animation_end: int) -> None:
    print(f'frames_num: {_frames_num}, bones_num: {_bones_num}')
    print(f'bones_list: {_bones_list}')
    print(f'animation begin: {_animation_begin}')
    print(f'animation end: {_animation_end}')


def unpack_struct(_form_in: str, _form_out: str, _data: list[int]) -> float | int:
    return unpack(_form_out, pack(_form_in, *_data))[0]
