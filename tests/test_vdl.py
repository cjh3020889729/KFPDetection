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
# Test vdlrecord class
import os
import sys
import numpy as np

# 设置当前KFPDetection包路径:
# 保证vdlrecords正常调用
sys.path.append( os.getcwd() )

from visualdl import LogReader
from vdlrecords import clear_vdlrecord_dir
from vdlrecords import ScalarVDL

if __name__ == "__main__":
    # 1.创建标量日志记录器
    recorder = ScalarVDL(
        logdir='vlogs',
        file_name='model.log',
        vdl_kind='scalar',
        tags=['train/loss'],
        display_name='train_ex1',
        resume_log=True
    )

    # 2.测试指定tag自动写入数据
    for i in range(100):
        recorder(
            tag='train/loss',
            data=i
        )

    # 3.不再使用/读取日志文件前进行文件写句柄的释放
    recorder.release()

    # 4.启动日志可视化
    recorder.run(port=7999, open_browser=True)

    # 5.读取写好的日志文件
    # log_path = os.path.join('vlogs', ScalarVDL.file_content+'scalar'+'.'+'model.log')
    # reader = LogReader(file_path=log_path)
    # 6.输出日志中的部分数据
    # print(reader.get_tags())
    # print(reader.get_data('scalar', 'train/loss')[-1])

    # 7.测试vdl日志目录的清理功能
    # clear_vdlrecord_dir(log_dir='vlogs', verbose=True)