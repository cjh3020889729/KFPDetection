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
# includes: vdlrecord class
from distutils.log import Log
import os
import sys
import numpy as np

from typing import Union

from loggers import create_logger
logger = create_logger(logger_name='vdlrecord')
try:
    from visualdl import LogWriter, LogReader
except :
    logger.warning("The visualdl can't import LogWriter.")
    raise ImportError()

__all__ = ['VDLCallback', 'ScalarVDL']


def clear_vdlrecord_dir(log_dir):
    """清空目标日志目录下的vdl日志文件
    """


class VDLCallback(object):
    log_base = 'vdlrecords.'
    def __init__(self,
                 logdir='vlogs',
                 file_name='',
                 vdl_kind='',
                 tags=['train/loss', 'eval/loss', 'test/loss'],
                 display_name=''):
        """visualdl日志器回调基类实现
            desc:
                Parameters:

                Returns:

        """
        super(VDLCallback, self).__init__()
        # 0.检查数据有效性
        # 0.1检查日志记录的tags是否有效
        if len(tags) == 0: # 检查需要记录的tag不为0个
            logger.error("The length of tags should be more than 0.")
            raise ValueError()

        # 1.拼接符合要求的日志文件名
        self.log_filename = file_name if file_name=='' \
            else self.log_base + vdl_kind + '.' + file_name
        # 2.检查日志文件名是否合理
        if self.log_filename!='': # 不为空时，检查是否为.log文件
            if not self.log_filename.endswith('.log'):
                logger.error("The vdllog file_name should be '' or xxxx.log.(file_name: {0})".format(
                    file_name))
                raise ValueError()
        
        # 3.创建vdl日志记录器
        self._writer = LogWriter(
            logdir=logdir,
            file_name=self.log_filename,
            display_name=display_name
        )
        
        # 4.创建记录器里每个tag记录用step参数
        #   随着对应tag在__call__中出现一次
        #   对应的step值+1
        self.tags_step = {k:0 for k in tags}
    
    def get_tags(self):
        """获取当前日志记录器支持的tag列表
            desc:
                Parameters:

                Returns:

        """
        return list(self.tags_step.keys())
    
    def release(self):
        """释放已创建的LogWriter
            desc:
                Parameters:

                Returns:

        """
        self._writer.close()

    def update(self,
               tag,
               data):
        """更新日志记录器中的写入数据(新添日志数据)
            desc:
                Parameters:

                Returns:

        """
    
    def __call__(self,
                 tag,
                 data):
        """执行回调，完成指定tag的日志数据写入
            desc:
                Parameters:

                Returns:
                    
        """
        if tag not in self.tags_step.keys():
            logger.error("The tag don't exist, while the vdlwriter init.(tag: {0})".format(
                tag))
            raise ValueError()
        self.update(tag=tag, data=data)

class ScalarVDL(VDLCallback):
    def __init__(self,
                 logdir='vlogs',
                 file_name='',
                 vdl_kind='scalar',
                 tags=['train/loss'],
                 display_name=''):
        super(ScalarVDL, self).__init__(
            logdir=logdir,
            file_name=file_name,
            vdl_kind=vdl_kind,
            tags=tags,
            display_name=display_name
        )
    
    def update(self, tag, data):
        """
        """
    



