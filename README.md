# ShadowFight3-Easy-Switch
## ShadowFight3 Animation Binary File Tool
### 使用方法(中文版)
&emsp;&emsp;在使用这个项目之前，你需要安装Python3.8或更新的版本，设置好Path环境变量（windows）并且安装numpy库（你可以使用`pip install numpy`命令来安装。配置好后你可以再命令行窗口键入以下命令
``` powershell
python /project_dir/sf3_bin_unpack_main.py [filepath(str)] [-o ISOLD(bool)]
```
&emsp;&emsp;参数解释
1. filepath：目标文件，即你想要转换的动作二进制文件的目录（str）。\n
2. -o(--isold): 可选参数，文件内的四元数是否经过压缩，默认为False（bool）。\n
&emsp;&emsp;以下是一个使用例子，转换新版本四元数已经经过压缩后的动作文件/target_filepath/anmation_binary.bytes。
``` powershell
python /project_dir/sf3_bin_unpack_main.py /target_filepath/anmation_binary.bytes -o False
```
