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
from datasets import ImageFolder

# 测试图片文件夹数据集加载
image_dataset = ImageFolder(
                    dataset_dir='tests',
                    image_dir='imgs',
                    sample_num=-1
                )
# 解析样本集
image_dataset.parse_dataset()
# 获取图片id到路径的映射字典
print(image_dataset.get_imid2path())
# 获取解析后数据集中的样本
print(image_dataset[0])