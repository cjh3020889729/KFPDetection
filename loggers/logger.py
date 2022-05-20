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
import sys, traceback

from typing import List, Union

__all__ = ['create_logger', 'get_created_logger_names', '_read_file_line', 'error_traceback']
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
        fmt="[%(asctime)s]\t-%(levelname)s-\t%(name)s: %(message)s",
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
            try:
                raise ValueError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=15,
                                num_lines=12)
                logger.error("Summary: The save_path should be a dir or ['*.txt', '*.log'].")
                sys.exit(1)

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


def _read_file_line(logger: logging.Logger,
                    file_path: str,
                    line: Union[int, List[int]]=0) -> None:
    """读取文件中指定行的内容并返回(去除首尾的空格与换行)
        desc:
            Parameters:
                logger: 用于参数检查异常的日志器(logging.Logger)
                file_path: 待读取文件的路径(str)
                line: 读取文件的指定行/行范围的信息(int or list[int])
                        eg: line=8 or line=[9, 12]
            Returns:
                None
    """
    # 1.检查数据是否合法
    if not(os.path.exists(file_path) and os.path.isfile(file_path)):
        try:
            raise ValueError()
        except:
            error_traceback(logger=logger,
                            lasterrorline_offset=6,
                            num_lines=1)
            logger.error("Summary: The file_path should be a file, and must exist.(path at: {0})".format(
                file_path))
            sys.exit(1)

    # 2.类型同步
    if isinstance(line, int): # 单行读取
        line = [line, line+1]
    else: # 数据检查: 多行读取(>=1)
        if not(len(line) == 2 and line[0] < line[1]):
            try:
                raise ValueError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=6,
                                num_lines=1)
                logger.error("Summary: The line only support be [start_line, end_line]"
                    "(start_line < end_line), while it's a list.(line={0})".format(line))
                sys.exit(1)

    # 3.读取指定行范围的数据
    line_strs = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        line_strs = f.readlines()[line[0]:line[1]]
    return '\t'.join(line_strs).strip() # 拼接行范围的数据并去掉首尾空白符

def error_traceback(logger: logging.Logger,
                    lasterrorline_offset: int=0,
                    num_lines: int=1) -> None:
    """利用日志器输出异常的回溯信息
        desc:
            Parameters:
                logger: 回溯文件使用的日志器(loggin.Logger)
                lasterrorline_offset: 最后一级有效回溯帧中实际错误信息所在行
                                      与帧中记录行的行偏移值(int)
                                      eg:
                                          error_traceback(): ')'所在行往前算
                num_lines: 展示最后一级有效回溯帧所在实际行+其后的共n行的信息
            Returns:
                None
    """
    # 1.获取最近抛出的异常形成的回溯数据
    _e_type, _, _tb = sys.exc_info()
    if _e_type == None: # None, 表示非有效异常或没有异常
        return
    # 2.由于回溯生成在该函数内，
    #   而实际异常发生在该函数外，
    #   因此，需要取最后一级回溯之前的堆栈信息
    _summarys = traceback.extract_stack()[:-1]

    # 3.取出最后一帧回溯
    last_summary = _summarys[-1]
    # 4.更新剩余回溯
    if len(_summarys) == 1: # 仅仅包含一帧回溯
        _summarys = []
    else: # 否则获取最后帧外的回溯
        _summarys = _summarys[:-1]

    # 5.遍历异常发出后栈中最后帧除外的回溯信息
    for _summary in _summarys:
        # 帧所在文件
        e_file = _summary.filename
        # 帧所在函数
        e_fcuntion_name = _summary.name
        # 帧目标行(回溯行)
        e_line = _summary.lineno
        # 利用日志器输出回溯信息
        logger.error("File {0}, Lines at {1}, in {2}\n\n\t{3}\n".format(
            e_file, e_line, e_fcuntion_name,
            _read_file_line(
                logger=logger,
                file_path=e_file,
                # 回溯帧目标行-1:
                # 由于帧行记录从1-n，读取文件行缓存的list序号从0-(n-1)
                # 因此帧行-1才能得到准确的行
                line=e_line - 1)))
    # 6.输出最后的回溯帧，需要修正偏移位置
    logger.error("File {0}, Lines at {1}, in {2}\n\n\t{3}\n".format(
            last_summary.filename, last_summary.lineno, last_summary.name,
            _read_file_line(
                logger=logger,
                file_path=last_summary.filename,
                # 6.1之所以-lasterrorline_offset:
                #   由于实际发生/抛出错误/异常行的
                #   实际行号在error_traceback()的')'之前
                # 6.2输入一个list[start_line, end_line]，获取连续行的信息
                line=[last_summary.lineno - 1 - lasterrorline_offset,
                      last_summary.lineno - 1 - lasterrorline_offset + num_lines])))