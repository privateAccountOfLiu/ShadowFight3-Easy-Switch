# ShadowFight3-Easy-Switch
## ShadowFight3 Animation Binary File Tool
### 使用方法(中文版)
&emsp;&emsp;在使用这个项目之前，你需要安装Python3.8或更新的版本，设置好Path环境变量（windows）并且安装numpy库（你可以使用`pip install numpy`命令来安装。配置好后你可以再命令行窗口键入以下命令：
``` powershell
python /project_dir/sf3_bin_unpack_main.py [filepath(str)] [-o ISOLD(bool)]
```
参数解释
1. filepath：目标文件，即你想要转换的动作二进制文件的目录（str）。
2. -o(--isold)：可选参数，文件内的四元数是否经过压缩，默认为False（bool）。

以下是一个使用例子，转换新版本四元数已经经过压缩后的动作文件`/target_filepath/anmation_binary.bytes`：
``` powershell
python /project_dir/sf3_bin_unpack_main.py /target_filepath/anmation_binary.bytes -o False
```
最后你可以在项目根目录找到输出结果`out_animation.csv`即`/project_dir/sf3_bin_unpack_main.py`。
***
### Usage Method(English Version)
Before using this project, you need to install Python 3.8 or newer versions, configure the PATH environment variable (for Windows), and install the numpy library (you can use the `pip install numpy` command). After configuration, you can enter the following command in the command line window:
``` powershell
python /project_dir/sf3_bin_unpack_main.py filepath(str) -o ISOLD(bool)
```
Parameter Explanation  
1. filepath: Target file directory of the motion binary file you want to convert (str).  
2. -o (--isold): Optional parameter indicating whether quaternions in the file are compressed. Default is False (bool).  

Usage Example  
To convert a compressed quaternion motion file from the new version located at `/target_filepath/anmation_binary.bytes`:  
``` powershell
python /project_dir/sf3_bin_unpack_main.py /target_filepath/anmation_binary.bytes -o False
```

The output file `out_animation.csv` will be generated in the project root directory, i.e., at `/project_dir/sf3_bin_unpack_main.py`.
