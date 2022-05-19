# 日志器接口实现说明

> Start Date: 2022.5.19
> 修订次数: 1
> End Date: 2022.5.19

分别设计INFO级日志器创建、获取当前程序创建的所有日志器名称的接口。

目录结构:
```
    |- __init__.py
    |- logger.py
```

接口分布:
```
    |- logger.py
        functions:
        |- create_logger
        |- get_created_logger_names
```

1. 对于INFO级日志器创建(logger.py):
    - 接口类型: 函数(create_logger)
    - 函数用途:
        - 创建一个INFO级的独立日志器(子父级日志器日志信息独立)
        - 支持字节流日志输出和文件流日志保存
    - 输入参数:
        - logger_name: 日志器名称
        - save_path: 日志文件流保存时的目录/日志文件
                     支持.txt与.log为念
    - 返回参数:
        - logging.Logger: 返回配置好的独立日志器
    - 函数解读:
        - 输入参数方面:
            - (logger_name)用于区分当前是否需要新建日志器
            
                同名日志器直接使用原始实例
            - (save_path)有时程序运行日志过多，保存在文件中可以避免丢失
        - 返回参数方面:
            - (logging.Logger)配置好的独立日志器可支持以下日志记录:
                日志器.info("xxxxx")
                日志器.warning("xxxxx")
                日志器.error("xxxxx")
                日志器.critical("xxxxx")

2. 对于获取当前程序创建的所有日志器名称(logger.py):
    - 接口类型: 函数(get_created_logger_names)
    - 函数用途:
        - 查看已创建日志器名称情况
        - 通过len(list)获取已有日志器数量
    - 输入参数:
        - None(无)
    - 返回参数:
        - list: 返回由所有日志器名称组成的列表
    - 函数解读:
        - 输入参数方面:
            - (前述充分，不再补充)
        - 返回参数方面:
            - (前述充分，不再补充)