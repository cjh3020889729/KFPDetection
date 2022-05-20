# 日志器接口实现说明

> Start Date: 2022.5.19
> 
> 修订次数: 2
> 
> End Date: 2022.5.20

分别设计INFO级日志器创建、获取当前程序创建的所有日志器名称以及执行异常回溯日志输出的接口。

目录结构:
```
    |- __init__.py
    |- logger.py
    |- README.md
```

接口分布:
```
    |- logger.py
        functions:
        |- create_logger
        |- get_created_logger_names
        |- _read_file_line
        |- error_traceback
```

1. 对于INFO级日志器创建(logger.py):
    - 接口类型: 函数(create_logger)
    - 函数用途:
        - 创建一个INFO级的独立日志器(子父级日志器日志信息独立)
        - 支持字节流日志输出和文件流日志保存
    - 输入参数:
        - logger_name: 日志器名称
        - save_path: 日志文件流保存时的目录/日志文件，支持.txt与.log为念

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

3. 对于执行异常回溯日志输出(logger.py):
    - 接口类型: 函数(error_traceback)
    - 函数用途:
        - 输出异常所生成的堆栈回溯信息
        - 输出具有层级的异常提示: 文件、行号、函数
        - 需要特别注意回溯最后一级的行号修正/行范围
    - 输入参数:
        - logger: 用于回溯文件输出的日志器(loggin.Logger)
        - lasterrorline_offset: 最后一级有效回溯帧中实际错误信息所在行

            与帧中记录行的行偏移值(int)

            eg:

            error_traceback(): ')'所在行往前算

        - num_lines: 展示最后一级有效回溯帧所在实际行+其后的共n行的信息
    - 返回参数:
        - None(无)
    - 函数解读:
        - 输入参数方面:
            - lasterrorline_offset可以修正最后一帧回溯信息指向的行，
            
            结合num_lines可以实现从最后一帧回溯真实行x到x+n-1行共n行的信息

        - 返回参数方面:
            - (前述充分，不再补充)

4. 对于获取回溯信息所指文件中的指定行/行范围信息(logger.py):
    - 接口类型: 函数(_read_file_line)
    - 函数用途:
        - 输出指定行/行范围的数据
        - 从第一行数据之后，每行数据前加一个\t
        - 然后将所有需要的行进行拼接
    - 输入参数:
        - logger: 用于函数入口参数检查异常输出的日志器(logging.Logger)
        - file_path: 待读取文件的路径(str)
        - line: 读取文件的指定行/行范围的信息(int or list[int])

            eg: line=8 or line=[9, 12]

    - 返回参数:
        - None(无)
    - 函数解读:
        - 输入参数方面:
            - (line)设定行时，要么单个数字，要么表示起点与终点行的行范围数据

                其中，终点务必大于起点。

        - 返回参数方面:
            - (前述充分，不再补充)