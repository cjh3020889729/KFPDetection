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

from typing import Any, Dict, List
from loggers import create_logger, error_traceback
logger = create_logger(logger_name=__name__)

__all__ = ['check_img_endswith', 'DetDataset', 'ImageFolder']


def check_img_endswith(img_file: str=None,
                           img_endswith: List[str]=[
                               'jpg', 'JPG', 'JPEG',
                               'png', 'PNG',
                               'bmp', 'BMP']) -> bool:
    """检查图片类型是否为支持的图片文件类型
        desc:
            Parameters:
                img_file: 图片文件路径(str)
                img_endswith: 支持的图像类型后缀(list(str))
            Returns:
                (bool)是否为支持的图片类型
    """
    if img_file.split('.')[-1] in img_endswith:
        return True
    logger.warning("The type of image file: {0} is not support.".format(img_file))
    return False

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
                    image_dir: 根目录下的图片所在目录/所在上一级目录(str)
                    anno_path: 根目录下的标注文件/标注说明文件路径(str)
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

        # 数据样本集: 初始化为None
        # None: 未解析数据
        self.samples = None
        # 数据预处理
        # None: 未配置任何预处理
        self.transforms = None
        # 数据集长度
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
    
    def set_kwargs(self, **kwargs) -> None:
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
                    (Dict[str, Any])样本数据
        """
        if self.samples == None: # 检查当前是否进行数据集解析
            try:
                raise ValueError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=6,
                                num_lines=1)
                logger.error("Summary: The self.samples is None."
                " Please firstly parse_dataset to update this parameter.")
                sys.exit(1)
        sample = self.samples[index]
        if self.transforms == None:
            return sample
        sample = self.transforms(sample)
        return sample
    
    def __len__(self) -> int:
        """返回数据集长度
            desc:
                Parameters:
                    None
                Returns:
                    (int)数据集长度
        """
        return self.length

class ImageFolder(Dataset):
    def __init__(self,
                 dataset_dir: str='',
                 image_dir: str='',
                 sample_num=-1,
                 **kwargs) -> None:
        """检测图像数据目录读取基类(继承用)——用于Test的预测数据加载
            desc:
                Parameters:
                    dataset_dir: 数据集根目录(str)
                    image_dir: 根目录下的图片目录(str)
                    sample_num: 在数据集中的采样数量(int)——-1表示全部数据
                Returns:
                    None
        """
        self.dataset_dir = dataset_dir
        self.image_dir = image_dir
        self.sample_num = sample_num
        self.kwargs = kwargs

        # 数据样本集: 初始化为None
        # None: 未解析数据
        self.samples = None
        # 数据预处理
        # None: 未配置任何预处理
        self.transforms = None
        # 数据集长度
        self.length = 0

    def parse_dataset(self) -> None:
        """解析数据集(self.samples)
            desc:
                Parameters:
                    None
                Returns:
                    None
        """
        self.samples = [] # 样本采样集
        self._imid2path = {} # 图片id与图片路径的映射dict
        # 1.解析目录下的图片
        images = self.get_images() # 获取所有图片的路径

        # 2.解析为样本集
        for idx, im in enumerate(images):
            self.samples.append({'im_id': idx, 'im_file': im})
            self._imid2path[idx] = im

        # 3.检查是否存在有效样本
        if len(self.samples) == 0:
            try:
                raise ValueError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=6,
                                num_lines=1)
                logger.error("Summary: The length of samples is zero,"
                    " so this dir({0}) hasn't any image file.".format(
                        os.path.join(self.dataset_dir, self.image_dir)))
                sys.exit(1)
        # 根据采样数量进行截取
        if self.sample_num != -1 and self.sample_num >= 0:
            if self.sample_num <= len(self.samples):
                self.samples = self.samples[:self.sample_num]
        self.length = len(self.samples) # 重置数据数据集长度
        logger.info("ImageFolder Dataset parse {0} samples.".format(self.length))
    
    def get_imid2path(self) -> Dict[int, str]:
        """获取图片id到路径的映射字典
            desc:
                Parameters:
                    None
                Returns:
                    (Dict[int, str])返回映射字典
        """
        return self._imid2path

    def get_images(self) -> List[str]:
        """获取数据集图片目录下的所有图片路径
            desc:
                Parameters:
                    None
                Returns:
                    (List[str])目录下所有图片的有效路径
        """
        image_dir_path = os.path.join(self.dataset_dir, self.image_dir)
        images = []
        for _, _, files in os.walk(image_dir_path):
            # 默认升序排序
            for _f in sorted(files):
                im_path = os.path.join(image_dir_path, _f)
                if check_img_endswith(img_file=im_path):
                    images.append(im_path)
            # 避免不同操作系统下的差异
            # 只读取当前层次目录的文件搜索
            break
        return images

    def set_transforms(self,
                       transforms: Any) -> None:
        """配置数据预处理
            desc:
                Parameters:
                    transforms: 预处理集合(Any)
                Returns:
                    None
        """
        self.transforms = transforms

    def __getitem__(self,
                    index: int) -> Dict[str, Any]:
        """获取数据集样本
            desc:
                Parameters:
                    index: 指定样本序号获取样本(int)
                Returns:
                    (Dict[str, Any])样本数据
        """
        if self.samples == None: # 检查当前是否进行数据集解析
            try:
                raise ValueError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=6,
                                num_lines=1)
                logger.error("Summary: The self.samples is None."
                " Please firstly parse_dataset to update this parameter.")
                sys.exit(1)
        sample = self.samples[index]
        if self.transforms == None:
            return sample
        sample = self.transforms(sample)
        return sample

    def __len__(self) -> int:
        """获取数据集长度
            desc:
                Parameters:
                    None
                Returns:
                    (int)数据集长度
        """
        return self.length