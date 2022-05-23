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
# Test dataset class/function
import os
import sys
import numpy as np

# 设置当前KFPDetection包路径:
# 保证datasets正常调用
sys.path.append( os.getcwd() )

from datasets import voc2coco

voc2coco(
    image_dir='C:\\Users\\30208\\Desktop\\KFPEducation\\tests\\dataset\\train\\IMAGES',
    anno_dir='C:\\Users\\30208\\Desktop\\KFPEducation\\tests\\dataset\\train\\ANNOTATIONS',
    train_ratio=0.99,
    output='tests/datasets'
)

