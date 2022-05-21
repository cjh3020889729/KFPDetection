# VDL日志器接口实现说明

> Start Date: 2022.5.20
> 
> 修订次数: 2
> 
> End Date: 2022.5.21

分别设计vdl日志记录基类、标量日志记录类。

目录结构:
```
    |- __init__.py
    |- vdlrecord.py
    |- README.md
```

接口分布:
```
    |- logger.py
        functions:
        |- clear_vdlrecord_dir
        classes:
        |- VDLCallback
        |- ScalarVDL
```

1. 对于vdl日志记录基类(logger.py):
    - 接口类型: 类(VDLCallback)
    - 类用途:
        - 作为所有vdl日志记录器的继承基类
    - 初始化参数:
        - logdir: 日志文件保存目录(str)
        - file_name: 日志文件名(str)
        - vdl_kind: 日志类型(str)
        - tags: 日志数据分类的tags(list(str))
        - display_name: 日志文件执行可视化时，日志文件显示的名称(str)
    - 类解读:
        - class.get_state: 获取日志器状态: True-正常, False-无效(需要重启reopen)
        - class.get_tags: 获取当前日志类中所有的tag
        - class.release: 释放当前的日志类中的
        - class.reopen: 如同初始化一样进行日志器重启
        - class.update: 更新记录一个日志数据(需要重载实现)
        - class.__call__: 实现类回调

2. 对于标量日志记录类(logger.py):
    - 接口类型: 类(ScalarVDL)
    - 类用途:
        - 作为vdl标量日志记录器的类
    - 初始化参数:
        - logdir: 日志文件保存目录(str)
        - file_name: 日志文件名(str)
        - vdl_kind: 日志类型(str)
        - tags: 日志数据分类的tags(list(str))
        - display_name: 日志文件执行可视化时，日志文件显示的名称(str)
    - 类解读:
        - class.get_state: 获取日志器状态: True-正常, False-无效(需要重启reopen)
        - class.get_tags: 获取当前日志类中所有的tag
        - class.release: 释放当前的日志类中的
        - class.reopen: 如同初始化一样进行日志器重启
        - class.update: 更新记录一个日志数据(实现标量日志数据记录)
        - class.__call__: 实现类回调

3.对于多余日志文件的清理(logger.py):
    - 接口类型: 函数(clear_vdlrecord_dir)
    - 函数用途:
        - 清理指定目录下，文件名包含特定content的文件
    - 输入参数:
        - log_dir: vdl日志文件目录(str)
        - split_content: 文件名划分字段的分隔符(str) -- 默认不用修改
        - file_content: 文件名主要组成字段(str) -- 默认不用修改
        - verbose: 是否显示运行时删除过程的详细信息(bool)
    - 返回参数:
        - None(无)
    - 函数解读:
        - 输入参数方面:
            - 由于当前vdl类中文件命名格式为: vdlrecords.xxxxx.log格式，
            - 因此无需更改分隔符与主要字段
        - 返回参数方面:
            - (None)清理完即可，无需返回