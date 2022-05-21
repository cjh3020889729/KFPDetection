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
import os, sys

from typing import List, Dict
from .det import DetDataset
from loggers import create_logger, error_traceback
logger = create_logger(logger_name=__name__)

__all__ = ['VOCDataset']


class VOCDataset(DetDataset):
    def __init__(self,
                 dataset_dir: str='',
                 image_dir: str='',
                 anno_path: str='',
                 data_fields: List[str]=['image'],
                 sample_num=-1,
                 label_list=None,
                 allow_empty=False,
                 empty_ratio=1.,
                 **kwargs):
        """VOC检测数据集解析加载类
            desc:
                Parameters:
                    dataset_dir: 数据集根目录(str)
                    image_dir: 根目录下的图片目录(str)
                    anno_path: 根目录下的标注目录(str)
                    data_fields: 样本数据采样的字典，非fields中指定的数据不保存(list(str))
                    sample_num: 在数据集中的采样数量(int)——-1表示全部
                    label_list: 目标类别列表(list(str))
                                如果不传入类别列表，则自动以类别id为label_name -> id2str
                    allow_empty: 支持采集没有一个目标的样本(bool)
                    empty_ratio: 空样本占有目标样本的数量比例(float: [0., 1.])
                                 在allow_empty为True时有效
                Returns:
                    None
        """
        super(VOCDataset, self).__init__(
            dataset_dir=dataset_dir,
            image_dir=image_dir,
            anno_path=anno_path,
            data_fields=data_fields,
            sample_num=sample_num,
            **kwargs
        )
        self.lable_list = label_list
        self.allow_empty = allow_empty
        self.empty_ratio = empty_ratio
    
    def parse_dataset(self) -> None:
        """解析VOC数据集
        """