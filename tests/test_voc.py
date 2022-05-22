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
# Test vocdataset class
import os
from datasets import VOCDataset, generate_Vocdataset_and_Voclable

# 1.测试voc格式数据的生成
# generate_Vocdataset_and_Voclable(
#     image_dir='C:\\Users\\30208\\Desktop\\KFPEducation\\tests\\dataset\\train\\IMAGES',
#     anno_dir='C:\\Users\\30208\\Desktop\\KFPEducation\\tests\\dataset\\train\\ANNOTATIONS',
#     train_ratio=0.75,
#     output='tests/dataset'
# )

# 2.测试VOC数据加载
dataset = VOCDataset(
    dataset_dir='tests/dataset',
    label_list='lable_list.txt',
    image_dir='VOCDataset',
    anno_path='train_list.txt',
    data_fields=['image'],
    sample_num=-1,
    allow_empty=False,
    empty_ratio=1.
)

dataset.parse_dataset()
print(dataset.get_cls2id())
print(dataset[0])