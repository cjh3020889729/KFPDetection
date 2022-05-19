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
# Test vdlrecord functions
import os
import sys
import numpy as np

# 设置当前KFPDetection包路径:
# 保证vdlrecords正常调用
sys.path.append( os.getcwd() )

from visualdl import LogReader
from vdlrecords import VDLCallback, ScalarVDL

recorder = VDLCallback(
    logdir='vlogs',
    file_name='model.log',
    vdl_kind='scalar',
    tags=['train/loss'],
    display_name='train_ex1'
)

for i in range(100):
    recorder(
        tag='train/loss',
        data=i
    )

recorder.release()

log_path = os.path.join('vlogs', VDLCallback.log_base+'scalar'+'.'+'model.log')
reader = LogReader(file_path=log_path)
print(reader.get_tags())
# print(reader.get_data('scalar', 'train/loss'))