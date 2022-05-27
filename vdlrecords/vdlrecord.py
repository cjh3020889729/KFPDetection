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
# 所有vdl日志类生成的日志文件格式均为:
# vdlrecords.系统自动生成.log
# 或者: vdlrecords.自定义日志文件名(vdlrecords.train_fcos.log)
import os
import sys
import numpy as np

from typing import Union, List, Any

from loggers import create_logger, error_traceback
logger = create_logger(logger_name='vdlrecord')
try:
    from visualdl import LogWriter, LogReader
    from visualdl.server import app
except :
    logger.warning("The visualdl can't import LogWriter.")
    raise ImportError()

__all__ = ['clear_vdlrecord_dir', 'VDLCallback', 'ScalarVDL']


def clear_vdlrecord_dir(log_dir: str='vlogs',
                        split_content: str='.',
                        file_content: str='vdlrecords',
                        verbose: bool=False) -> None:
    """清空目标日志目录下的vdl日志文件
        desc:
            Parameters:
                log_dir: vdl日志文件目录(str)
                split_content: 文件名划分字段的分隔符(str) -- 默认不用修改
                              eg: '.' --> 'file.txt' => ['file', 'txt']
                file_content: 文件名主要组成字段(str) -- 默认不用修改
                              eg: 'vdlrecords' -->
                                  vdlrecords.1321415.log =>
                                  ['vdlrecords', '1321415', 'log']
                verbose: 是否显示运行时删除过程的详细信息(bool)
            Returns:
                None
    """
    if not os.path.isdir(log_dir): # 待清空日志路径不是目录
        try:
            raise ValueError()
        except:
            error_traceback(logger=logger,
                            lasterrorline_offset=6,
                            num_lines=1)
            logger.error("Summary: The log_dir should be a dir, but now it's not.(path at: {0})".format(
                log_dir))
            sys.exit(1)
    if not os.path.exists(log_dir): # 待清空目录不存在
        logger.warning('The log_dir is not exist.(path at: {0})'.format(
            log_dir))
        return
    # 遍历目录下的所有文件
    clear_num = 0 # 清楚日志文件数量
    for _, _, files in os.walk(log_dir):
        for vdl_f in files:
            file_contents = vdl_f.split(split_content) # 按照split_content分割文件
            # 按照所选文件名必须包含file_content来筛选
            # 如果content出现在当前文件中，则进行清楚
            if file_content in file_contents:
                rm_path = os.path.join(log_dir, vdl_f)
                os.remove(rm_path)
                clear_num += 1
                if verbose:
                    logger.info('Removing the vdl_logfile: {0}.'.format(rm_path))
            else: # 不存在，则跳过清理
                continue
    if verbose:
        logger.info('The vdlrecord dir has cleared {0} vdl_log files.'.format(clear_num))


class VDLCallback(object):
    file_content = 'vdlrecords.'
    def __init__(self,
                 logdir: str='vlogs',
                 file_name: str='',
                 vdl_kind: str='',
                 tags: List[str]=['train/loss', 'eval/loss', 'test/loss'],
                 display_name: str='',
                 resume_log: bool=False) -> None:
        """visualdl日志器回调基类实现
            desc:
                Parameters:
                    logdir: 日志保存的目录(str)
                    file_name: 日志文件名(str, 如果为''，则自动生成文件名)
                               eg: file_name --> name.log
                    vdl_kind: 当前vdl记录数据的格式(str)
                              支持以下格式:
                                - scalar: 标量记录(损失、学习率等标量数据)
                                - image: 特征图/图像记录(预处理图像、特征图分析等)
                                - histogram: 直方图数据记录(权重、梯度等张量数据)
                                - pr_curve: PR曲线
                                - roc_curve: roc曲线
                               使用时务必指定，不能为''
                    tags: 日志器需要记录的不同数据的标识字段(List(str))
                    display_name: 日志可视化界面中显示的日志名称(str)
                    resume_log: 是否续写日志(日志已经存在则支持)
                Returns:
                    None
        """
        super(VDLCallback, self).__init__()
        # 0.检查数据有效性
        # 0.1检查日志记录的tags是否有效
        if len(tags) == 0: # 检查需要记录的tag不为0个
            try:
                raise ValueError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=6,
                                num_lines=1)
                logger.error("Summary: The length of tags should be more than 0.(tags: {0})".format(
                    tags))
                sys.exit(1)

        # 0.2基本属性配置
        self.resume_log = resume_log
        self.vdl_kind = vdl_kind
        # 0.3.创建记录器里每个tag记录用step参数
        #   随着对应tag在__call__中出现一次
        #   对应的step值+1
        self.tags_step = {k:0 for k in tags}

        # 1.拼接符合要求的日志文件名
        self.logdir = logdir
        self.log_filename = file_name if file_name=='' \
            else self.file_content + vdl_kind + '.' + file_name
        # 2.检查日志文件名是否合理
        if self.log_filename!='': # 不为空时，检查是否为.log文件
            if not self.log_filename.endswith('.log'):
                try:
                    raise ValueError()
                except:
                    error_traceback(logger=logger,
                                    lasterrorline_offset=7,
                                    num_lines=2)
                    logger.error("Summary: The vdllog file_name should be '' or xxxx.log.(file_name: {0})".format(
                        file_name))
                    sys.exit(1)
        
        # 3.更新日志数据(tags_step或log_file)--根据是否续写
        self._reload_vdllog()
        
        # 4.创建vdl日志记录器
        self._writer = LogWriter(
            logdir=logdir,
            file_name=self.log_filename,
            display_name=display_name
        )
        self.writer_state = True # 日志记录器开启状态

    def _reload_vdllog(self):
        """重新生成日志(清空已有数据/更新tags_step)
            desc:
                Parameters:
                    None
                Returns:
                    None
                Others:
                    - 续写则进行step更新
                    - 不续写则进行日志文件删除
        """
        if self.resume_log == False: # 非续写--清空
            log_path = os.path.join(self.logdir, self.log_filename)
            if os.path.isfile(log_path): # 日志存在
                logger.warning("The log file: {0} will be recreated.".format(log_path))
                os.remove(path=log_path)
        else:
            log_path = os.path.join(self.logdir, self.log_filename)
            if os.path.isfile(log_path): # 日志存在
                reader = LogReader(file_path=log_path)
                _kinds = reader.get_tags()
                if len(_kinds) <= 1:
                    try:
                        raise ValueError()
                    except:
                        error_traceback(logger=logger,
                                        lasterrorline_offset=6,
                                        num_lines=1)
                        logger.error("Summary: The _kinds: {0} have not truth data kind.".format(
                            _kinds) + \
                            "Maybe the log_file: {1} is empty.".format(
                            log_path))
                        sys.exit(1)
                _tags = _kinds[self.vdl_kind]
                for tag in _tags: # 更新tag的step
                    if tag in self.tags_step.keys():
                        _step = reader.get_data(self.vdl_kind, tag)[-1].id
                        self.tags_step[tag] = _step + 1
                        logger.info("The log tag: {0} has updated the step-{1}.".format(
                            _tags, _step + 1))

    def get_state(self) -> bool:
        """获取当前日志器状态
            desc:
                Parameters:
                    None
                Return:
                    (bool)当前日志器状态
        """
        return self.writer_state
    
    def get_tags(self) -> List[str]:
        """获取当前日志记录器支持的tag列表
            desc:
                Parameters:
                    None
                Returns:
                    (list(str))日志器的tags
        """
        return list(self.tags_step.keys())
    
    def release(self) -> None:
        """释放已创建的LogWriter
            desc:
                Parameters:
                    None
                Returns:
                    None
        """
        if self.writer_state == False:
            logger.warning("The visualdl writer has finished to work,"
                " so it can't stop again.")
        else:
            self._writer.close()
            del self._writer
            self._writer = None
            self.writer_state = False # 日志记录器关闭/失效状态
    
    def reopen(self, logdir: str='vlogs',
                     file_name: str='',
                     vdl_kind: str='',
                     tags: List[str]=['train/loss', 'eval/loss', 'test/loss'],
                     display_name: str='') -> None:
        """重启日志器
            desc:
                Parameters:
                    logdir: 日志保存的目录(str)
                    file_name: 日志文件名(str, 如果为''，则自动生成文件名)
                               eg: file_name --> name.log
                    vdl_kind: 当前vdl记录数据的格式(str)
                              支持以下格式:
                                - scalar: 标量记录(损失、学习率等标量数据)
                                - image: 特征图/图像记录(预处理图像、特征图分析等)
                                - histogram: 直方图数据记录(权重、梯度等张量数据)
                                - pr_curve: PR曲线
                                - roc_curve: roc曲线
                               使用时务必指定，不能为''
                    tags: 日志器需要记录的不同数据的标识字段(List(str))
                    display_name: 日志可视化界面中显示的日志名称(str)
                Returns:
                    None
        """
        if self.writer_state == True: # 本身写入器还在工作
            self.release() # 释放已有日志写入器
        
        # 总是重调init完成初始化和当前对象的写入器重建
        self.__init__(logdir=logdir,
                      file_name=file_name,
                      vdl_kind=vdl_kind,
                      tags=tags,
                      display_name=display_name)

    def update(self,
               tag: str,
               data: Any) -> None:
        """更新日志记录器中的写入数据(新添日志数据--继承需实现)
            desc:
                Parameters:
                    tag: 当前数据所属tag(str)
                    data: 日志记录的数据(对应记录器的数据)
                Returns:
                    None
        """
        try:
            raise NotImplementedError()
        except:
            error_traceback(logger=logger,
                            lasterrorline_offset=16,
                            num_lines=13)
            logger.error("Summary: The update function of"
            " '{0}' class should be reload or implement.".format(self.__class__.__name__))
            sys.exit(1)
    
    def run(self,
            port: int=8040,
            open_browser: bool=False) -> None:
        """启动日志可视化: 可手动打开浏览器输入: localhost:port号(eg: localhost:8040)
            desc:
                Parameters:
                    port: 本地服务的端口号(自定义7000-9000即可)
                    open_browser: 启动服务后自动打开浏览器
                Returns:
                    None
                Others:
                    - 需要在__name__=="__main__"中运行
        """
        app.run(logdir=self.logdir,
                port=port,
                open_browser=open_browser)
    
    def __call__(self,
                 tag: str,
                 data: Any,
                 step: int=None) -> None:
        """执行回调，完成指定tag的日志数据写入
            desc:
                Parameters:
                    tag: 当前数据所属tag(str)
                    data: 日志记录的数据(对应记录器的数据)
                    step: 使用指定的step进行数据更新(一般为续写)
                Returns:
                    None
        """
        if self.writer_state == False: # 检查工作状态
            try:
                raise AssertionError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=6,
                                num_lines=3)
                logger.error("Summary: The writer_state is False, so vdlrecord's update order can't work.")
                sys.exit(1)
        if tag not in self.tags_step.keys(): # 检查tag是否有效
            try:
                raise ValueError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=6,
                                num_lines=1)
                logger.error("Summary: The tag don't exist, while the vdlwriter init.(tag: {0})".format(
                    tag))
                sys.exit(1)

        # 如果指定step，则更新对应tag下的step
        if step is not None:
            self.tags_step[tag] = step

        self.update(tag=tag, data=data)

        self.tags_step[tag] += 1 # 更新为下一次待写入的step

class ScalarVDL(VDLCallback):
    def __init__(self,
                 logdir: str='vlogs',
                 file_name: str='',
                 vdl_kind: str='',
                 tags: List[str]=['train/loss'],
                 display_name: str='',
                 resume_log: bool=False) -> None:
        """标量日志记录器
        """
        super(ScalarVDL, self).__init__(
            logdir=logdir,
            file_name=file_name,
            vdl_kind=vdl_kind,
            tags=tags,
            display_name=display_name,
            resume_log=resume_log
        )
    
    def update(self,
               tag: str,
               data: Any) -> None:
        """更新日志记录器中的标量写入数据
            desc:
                Parameters:
                    tag: 当前数据所属tag(str)
                    data: 日志记录的数据(对应记录器的数据)
                Returns:
                    None
        """
        # 写入日志文件
        self._writer.add_scalar(tag=tag,
                                value=data,
                                step=self.tags_step[tag])



