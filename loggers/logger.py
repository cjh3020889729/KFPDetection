# Copyright (c) 2022 Jinghui Cai. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# includes: create logger functions
import logging
import os
import sys

from typing import Union

__all__ = ['create_logger', 'get_created_logger_names']
created_logger_names = []

def create_logger(logger_name: str='kfpdet',
                  save_path: Union[str, None]=None) -> logging.Logger:
    """创建一个INFO-logger日志器(支持info，warning，error，critical)
        desc:
            Parameters:
                logger_name: 日志器名字(str)
                save_path: 日志信息保存文件路径(str)
                           支持txt与log类型的文件名和目录
                           为目录时，在目录下自动创建log.txt
            Returns:
                返回已经配置好处理器的日志器(logging.Logger)
            Others:
                logger level:
                    CRITICAL: 50
                    ERROR: 40
                    WARNING: 30
                    INFO: 20
                    DEBUG: 10
                    NOTSET: 0
                logger关联特性:
                    类似于包命令空间所属的形式:
                    如日志器'foo', 'foo.bar', 'foo.baz'中，
                    后两者都是foo的子级记录器，与foo存在关联
    """
    # 1.创建日志(记录)器
    # 1.1根据日志名创建一个日志器
    #   如果name重复，返回已有实例
    #   不重复创建
    logger = logging.getLogger(name=logger_name)
    # 1.2已经存在的logger，直接返回
    if logger_name in created_logger_names:
        return logger

    # 2.配置日志器参数
    # 2.1设置日志器(记录器)级别
    #   默认级别为: WARNING
    #   设置级别为: INFO
    #   记录器只记录大于等于记录器等级的日志信息，并发送给处理器
    logger.setLevel(logging.INFO)
    # 2.2保持日志器信息相互独立，关联日志器间日志信息不传播
    #   避免日志信息记录混乱
    #   如: pkg1.test1与pkg1这样的子父级关联日志器间不再传播信息
    #   默认开启，会导致记录的日志信息在关联的日志信息之间传播
    logger.propagate = False

    # 3.构建日志器内处理器的格式器
    #   [时间] 当前日志信息的级别-日志记录器名称: 日志信息
    #   时间格式: 年-月-日 时-分-秒
    log_formatter = logging.Formatter(
        fmt="[%(asctime)s] -%(levelname)s-\t%(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 4.添加处理器(处理器日志等级小于等于记录器等级)
    # 4.1添加用于程序正常运行调试记录的字节流处理器
    #   字节流输出定向为: 标准输出
    #   字节流处理器设日志级别为: DEBUG
    #   前面设置记录器的级别为INFO，
    #   因此可以实现记录的日志信息传递到该处理进行日志处理输出
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    # 4.2添加用于文件格式记录程序正常运行调试记录的文件流处理器
    #   文件流输出定向为: save_path
    #   文件流处理器设日志级别为: DEBUG
    if save_path is not None: # 设置日志输出文件时，才执行添加
        # 判断文件是否符合要求
        if os.path.isfile(save_path) and \
           ( save_path.endswith('.txt') or save_path.endswith('.log') ):
           log_filename = save_path
        elif os.path.isdir(save_path): # 目录情况
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            log_filename = os.path.join(save_path, 'log.txt')
        else:
            raise ValueError("output should be a dir or ['*.txt', '*.log']")

        file_handler = logging.FileHandler(filename=log_filename, mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)
    
    # 5.记录日志器
    created_logger_names.append(logger_name)
    # 6.返回日志器
    return logger

def get_created_logger_names() -> list:
    """获取所有已创建的日志器名字
        desc:
            Parameters:
                None
            Returns:
                包含日志器名称的列表(list)
    """
    return created_logger_names

