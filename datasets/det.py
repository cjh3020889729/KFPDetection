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
import os,sys
from paddle.io import Dataset

from typing import Any, Union, Dict, List
from loggers import create_logger, error_traceback
logger = create_logger(logger_name=__name__)

__all__ = []


class DetDataset(Dataset):
    def __init__(self,
                 dataset_dir: str='',
                 image_dir: str='',
                 anno_path: str='',
                 data_fields: List[str]=['image'],
                 sample_num=-1,
                 **kwargs) -> None:
        """检测数据集解析加载基类(继承用)
            desc:
                Parameters:
                    dataset_dir: 数据集根目录(str)
                    image_dir: 根目录下的图片目录(str)
                    anno_path: 根目录下的标注目录(str)
                    data_fields: 样本数据采样的字典，非fields中指定的数据不保存(list(str))
                    sample_num: 在数据集中的采样数量(int)
                Returns:
                    None
        """
        super(DetDataset, self).__init__()
        self.dataset_dir = dataset_dir
        self.image_dir = image_dir
        self.anno_path = anno_path
        self.data_fields = data_fields
        self.sample_num = sample_num
        self.kwargs = kwargs # 其它可能需要的参数位

        # 样本的数量
        self.length = 0
    
    def get_anno(self) -> str:
        """获取标注文件的真实路径
            desc:
                Parameters:
                    None
                Return:
                    (str)标注文件完整路径——dir or file_path
        """
        return os.path.join(self.dataset_dir, self.anno_path)
    
    def parse_dataset(self) -> None:
        """解析检测数据集得到样本集(self.samples)——解析数据时需要实现
            desc:
                Parameters:
                    None
                Returns:
                    None
        """
        try:
            raise NotImplementedError()
        except:
            error_traceback(logger=logger,
                            lasterrorline_offset=13,
                            num_lines=10)
            logger.error("Summary: The parse_dataset function of"
            "'{0}' class should be reload or implement.".format(self.__class__.__name__))
            sys.exit(1)
    
    def set_transform(self,
                      transforms: Any) -> None:
        """配置样本预处理方法
            desc:
                Parameters:
                    transforms: 预处理集合(Any)
                Returns:
                    None
        """
        self.transforms = transforms
    
    def set_kwargs(self, **kwargs):
        """添加参数项(需要添加参数项时实现)
            desc:
                Parameters:
                    **kwargs: 参数项(dict)
                Returns:
                    None
        """
        try:
            raise NotImplementedError()
        except:
            error_traceback(logger=logger,
                            lasterrorline_offset=13,
                            num_lines=10)
            logger.error("Summary: The set_kwargs function of"
            "'{0}' class should be reload or implement.".format(self.__class__.__name__))
            sys.exit(1)

    def __getitem__(self, index: int) -> Dict[str, Any]:
        """获取单个样本
            desc:
                Parameters:
                    index: 指定样本序号获取样本(int)
                Returns:
                    None
        """
        sample = self.samples[index]
        sample = self.transforms(sample)
        return sample
    
    def __len__(self) -> int:
        """返回数据集长度
            desc:
                Parameters:
                    None
                Returns:
                    None
        """
        return self.length

class ImageFolder(Dataset):
    def __init__(self):
        """
        """
    
    def parse_dataset(self):
        """
        """
    
    def __getitem__(self, index):
        """
        """
    
    def __len__(self):
        """
        """
    