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
# includes: about vocdataset functions
import os, sys
import shutil
import numpy as np
from xml.etree import ElementTree as ET

from typing import List, Dict, Any

from .det import DetDataset, check_img_endswith
from loggers import create_logger, error_traceback
logger = create_logger(logger_name=__name__)

__all__ = ['generate_Vocdataset_and_Voclable', 'VOCDataset']


def generate_Vocdataset_and_Voclable(image_dir: str,
                                     anno_dir: str,
                                     train_ratio: float=0.7,
                                     output: str='.') -> None:
    """生成VOC数据集以及lable_list
        desc:
            Parameters:
                image_dir: 原始图片文件目录(str)
                            |- image_dir
                               |- imagex.jpg....
                anno_dir: 原始标注文件目录(str)
                            |- anno_dir
                               |- imagex.xml....
                train_ratio: 训练集占比(float)
                output: 实际输出目录，至少为'.'(str) —— 务必指定
                            |- output_上一级的目录
                               |- output最后一级的目录
                                  |- JPEGImages...
            Returns:
                None
    """
    import time
    start_time = time.time()
    logger.info("Starting generate VOC Dataset dir.")
    # 1.解析处理的样本集: [[img, xml]...]
    records = []
    for _, _, img_files in os.walk(image_dir):
        anno_files = []
        for _, _, annos in os.walk(anno_dir):
            for anno in annos:
                if anno.endswith('.xml') or anno.endswith('.XML'):
                    anno_files.append(anno)
                else:
                    logger.warning("The annotation file: {0} is not a xml file.".format(
                        os.path.join(anno_dir, anno)))
            break
        for img in img_files:
            if not check_img_endswith(img_file=img):
                logger.warning("The image file: {0} can't be supported.".format(
                    os.path.join(image_dir, anno)))
                continue
            for idx, anno in enumerate(anno_files):
                if img.split('.')[0] == anno.split('.')[0]:
                    records.append([img, anno])
                    anno_files.pop(idx)
                    break
        break

    # 2.生成目标目录
    if not os.path.isdir(output): # 目录不存在
        os.makedirs(output)
    dist_image_dir = os.path.join(os.path.join(output, 'VOCDataset'), 'JPEGImages')
    dist_anno_dir = os.path.join(os.path.join(output, 'VOCDataset'), 'Annotations')
    if not os.path.isdir(dist_image_dir):
        os.makedirs(dist_image_dir)
    if not os.path.isdir(dist_anno_dir):
        os.makedirs(dist_anno_dir)

    # 3.拷贝文件到目标目录，同时记录样本信息
    logger.info("Start copy source file to dist dataset dir.")
    lable_list = set() # 所有样本的类别
    dist_image_anno_list = [] # 所有样本的路径信息
    for idx, record in enumerate(records):
        # 读取前期的样本记录
        img, anno = record
        # 生成完整的源文件路径与目标路径
        img_origin = os.path.join(image_dir, img)
        img_dist = os.path.join(dist_image_dir, img)
        anno_origin = os.path.join(anno_dir, anno)
        anno_dist = os.path.join(dist_anno_dir, anno)
        # 完成文件拷贝
        shutil.copyfile(img_origin, img_dist)
        shutil.copyfile(anno_origin, anno_dist)
        # 记录目标样本数据路径
        dist_image_anno_list.append(
            os.path.join('JPEGImages', img) + ' ' + \
            os.path.join('Annotations', anno) + '\n'
        ) # img_path + ' ' + anno_path + '\n'
        # 读取xml标注文件，收集class/lable情况
        tree = ET.parse(anno_dist)
        objs = tree.findall('object')
        if len(objs) == 0:
            continue
        for obj in objs: # 遍历所有目标，获取类名的集合set
            lable_list.add(obj.find('name').text)
        if (idx+1) % int(len(records)*0.2) == 0:
            logger.info("Copy source file: {0} / {1}.".format(
                idx + 1, len(records)))

    # 4.保存样本信息以及类别信息
    import random
    random.shuffle(dist_image_anno_list)
    total_num = min(int(len(dist_image_anno_list)*train_ratio), len(dist_image_anno_list))
    train_list = dist_image_anno_list[:int(total_num*train_ratio)]
    if total_num == len(dist_image_anno_list): # 如果训练集取完样本集了，则验证集为空
        eval_list = []
    else:
        eval_list = dist_image_anno_list[int(total_num*train_ratio):]
    with open(os.path.join(output, 'train_list.txt'), 'w') as f:
        f.writelines(train_list)
    logger.info("The Dataset has generate {0} samples for Train.".format(
        len(train_list)))
    with open(os.path.join(output, 'eval_list.txt'), 'w') as f:
        f.writelines(eval_list)
    logger.info("The Dataset has generate {0} samples for Eval.".format(
        len(eval_list)))
    with open(os.path.join(output, 'lable_list.txt'), 'w') as f:
        for lable in lable_list:
            f.write(lable + '\n')
    logger.info("The Dataset has {0} classes.".format(
        len(lable_list)))
    logger.info("Dist Dataset Dir Tree:\n"
        "|- {0}\n\t|- {1}\n\t\t|- {2}\n\t\t|- {3}\n\t\t|- {4}\n\t\t|- {5}\n\t\t|- {6}".format(
            os.path.abspath(output), 'VOCDataset',
            'JEPGImages', 'Annotations',
            'train_list.txt', 'eval_list.txt', 'lable_list.txt'))
    logger.info("Total cost: {0:.2f}s.".format(time.time() - start_time))

class VOCDataset(DetDataset):
    def __init__(self,
                 dataset_dir: str,
                 label_list: str,
                 image_dir: str='',
                 anno_path: str='',
                 data_fields: List[str]=['image'],
                 sample_num=-1,
                 allow_empty=False,
                 empty_ratio=1.,
                 **kwargs):
        """VOC检测数据集解析加载类
            desc:
                Parameters:
                    dataset_dir: 数据集根目录(str)
                    label_list: 类别文件路径(str)
                               |- dataset_dir: 数据集根目录
                                  |- image_dir: 图片根目录
                                     |- Images: 图片文件夹
                                     |- Annos: 标注文件夹
                                  |- anno_path: 标注说明文件
                                  |- label_list: 类别统计txt文件
                    image_dir: 根目录下的图片所在目录/所在上一级目录(str)
                               |- dataset_dir: 数据集根目录
                                  |- image_dir: 图片根目录
                                     |- Images: 图片文件夹
                                     |- Annos: 标注文件夹
                                  |- anno_path: 标注说明文件
                                  |- label_list: 类别统计txt文件
                    anno_path: 根目录下的标注文件/标注说明文件路径(str)
                               |- dataset_dir: 数据集根目录
                                  |- image_dir: 图片根目录
                                     |- Images: 图片文件夹
                                     |- Annos: 标注文件夹
                                  |- anno_path: 标注说明文件
                                  |- label_list: 类别统计txt文件
                    data_fields: 样本数据采样的字典，非fields中指定的数据不保存(list(str))
                    sample_num:  在数据集中的样本的采样数量(int)——-1表示全部样本
                    allow_empty: 支持采集没有一个目标的样本(bool)——空样本
                    empty_ratio: 空样本占有目标样本的数量比例(float: [0., 1.])
                                 在allow_empty为True时有效
                Returns:
                    None
                Others:
                    - 解析数据集目录结构为:
                        |- dataset_dir
                            |- image_dir
                                |- 存放标注文件的目录(eg: Annotations)
                                |- 存放图片文件的目录(eg: JPEGImages)
                            |- anno_path: 标注说明文件
                                eg:
                                    train_list.txt
                                        ```
                                        图片路径 对应的标注路径
                                        ...
                                        ```
                                    图片路径(eg: JPEGImages/image1.jpg)
                                    标注路径(eg: Annotations/image1.xml)
                            |- lable_list: 类别文件路径
                                eg:
                                    lable_list.txt
                                        ```
                                        label1
                                        label2
                                        ...
                                        ```
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
    
    def _sample_empty(self,
                      records: Dict[str, Any],
                      num: int) -> Dict[str, Any]:
        """采样一定数量没有目标的样本(空样本)
            desc:
                Parameters:
                    records: 没有目标的样本集(Dict[str, Any])
                    num: 有目标的样本数量(int)
                Returns:
                    (Dict[str, Any])采样后的空样本
        """
        if self.empty_ratio < 0. or self.empty_ratio >=1.:
            return records
        import random
        sample_num = min(len(records), num*self.empty_ratio)
        empty_samples = random.sample(records, k=sample_num)
        return empty_samples

    def parse_dataset(self) -> None:
        """解析VOC数据集(self.samples)
            desc:
                Parameters:
                    None
                Returns:
                    None
        """
        import time
        start_time = time.time()
        logger.info("Starting the VOC Dataset.")
        # 1.配置标注说明文件的路径以及图片所在目录
        anno_path = self.get_anno()
        image_dir = os.path.join(self.dataset_dir, self.image_dir)

        # 2.配置缓存参数
        records = [] # 有目标样本的缓存
        empty_records = [] # 没有目标样本的缓存
        count = 0 # 实际样本计数
        cls2id = {} # 类别到id的映射字典
        # 记录类别id的集合
        # 用于记录当前解析数据集的类别id情况
        # 当self.lable_list为None时，
        # 利用该参数最后生成cls2id映射字典
        cls_records = set()
        if self.lable_list: # 解析类别到id的映射字典
            label_path = os.path.join(self.dataset_dir, self.lable_list)
            if not os.path.isfile(label_path):
                try:
                    raise ValueError()
                except:
                    error_traceback(logger=logger,
                                    lasterrorline_offset=8,
                                    num_lines=3)
                    logger.error("Summary: The file of label_path does"
                        " not exist.(path at: {0})".format(label_path))
                    sys.exit(1)
            with open(label_path, 'r') as f:
                clses = f.readlines()
                for idx, _cls in enumerate(clses):
                    cls2id[_cls.strip()] = idx
        else:
            try:
                raise ValueError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=22,
                                num_lines=19)
        logger.info("Finished class statistics.")
        
        # 打开标注说明文件(train_list.txt等)
        # 其中每一行都表示一个样本的图片+' '+标注文件
        with open(anno_path, 'r') as f:
            for line in f.readlines():
                # 解析出图片、标注文件的真实路径
                img_file, xml_file = [
                    os.path.join(image_dir, x) \
                        for x in line.strip().split(' ')[:2]
                ]
                if not os.path.isfile(img_file): # 检查是否存在且为文件
                    logger.warning("The image file: {0}, it does not exist.".format(img_file))
                    continue
                if not os.path.isfile(xml_file): # 检查是否存在且为文件
                    logger.warning("The xml file: {0}, it does not exist.".format(xml_file))
                    continue

                # 解析标注的xml文件
                tree = ET.parse(xml_file)
                # 查看标注文件中的size基本元素
                im_size = tree.find('size')
                if im_size == None: # 检查xml文件是否完整，具备基本的元素
                    logger.warning("The xml file: {0},".format(xml_file) + \
                        " it hasn't size element in xml parse-tree.")
                    continue
                # 获取图片的宽高
                im_w = float(tree.find('size').find('width').text)
                im_h = float(tree.find('size').find('height').text)
                # 检查宽高是否要求
                if im_w < 0 or im_h < 0:
                    logger.warning("The im_w({0}) or im_h({1})".format(im_w, im_h) + \
                        " in xml file: {2}, it's not right.".format(xml_file))
                    continue
                # 获取图片标注的所有目标
                objs = tree.findall('object')

                # 遍历目标获取标注数据
                # 文件中obj数量与实际有效bbox的计数
                num_bbox, bbox_count = len(objs), 0
                # 利用文件中obj数量设置统计量的基本长度
                # 后期使用实际计数进行剪切获取真实数据
                gt_bbox = np.zeros((num_bbox, 4), dtype=np.float32)
                gt_class = np.zeros((num_bbox, 1), dtype=np.int32)
                gt_score = np.zeros((num_bbox, 1), dtype=np.float32)
                difficult = np.zeros((num_bbox, 1), dtype=np.int32)
                for obj in objs:
                    # 1.获取类名
                    cls_name = obj.find('name').text
                    # 2.查看目标是否存在困难目标的描述——没有统一为0
                    #   否则使用实际标注值
                    _difficult = obj.find('difficult')
                    _difficult = int(_difficult.text) \
                        if _difficult is not None else 0
                    # 3.获取边界框坐标
                    x1 = float(obj.find('bndbox').find('xmin').text)
                    y1 = float(obj.find('bndbox').find('ymin').text)
                    x2 = float(obj.find('bndbox').find('xmax').text)
                    y2 = float(obj.find('bndbox').find('ymax').text)
                    # 4.矫正坐标值
                    x1 = max(x1, 0)
                    y1 = max(y1, 0)
                    x2 = min(im_w - 1, x2)
                    y2 = min(im_h - 1, y2)
                    # 5.判断标注边界框位置是否合理
                    if x2 > x1 and y2 > y1:
                        gt_bbox[bbox_count, :] = [x1, y1, x2, y2]
                        gt_class[bbox_count, 0] = cls2id[cls_name]
                        gt_score[bbox_count, 0] = 1.
                        difficult[bbox_count, 0] = _difficult
                        bbox_count += 1
                    else:
                        logger.warning("The bbox([{0}, {1}, {2}, {3}])".format(
                            x1, y1, x2, y2) + \
                            " in xml file: {0}".format(xml_file) + \
                            ", it hasn't error.")
                # 根据实际解析到的边界框数量来切片真实数据
                gt_bbox = gt_bbox[:bbox_count]
                gt_score = gt_score[:bbox_count]
                gt_class = gt_class[:bbox_count]
                difficult = difficult[:bbox_count]

                # voc样本的基本参数记录(当解析需要包含图片信息时的模板)
                voc_record = {
                    'im_file': img_file, # 样本图片路径
                    'im_id': count, # 分配的图片id
                    'h': im_h, # 图片高
                    'w': im_w, # 图片宽
                } if 'image' in self.data_fields else {}
                # 真实标注的参数记录
                gt_record = {
                    'gt_bbox': gt_bbox,
                    'gt_class': gt_class,
                    'gt_score': gt_score,
                    'difficult': difficult
                }
                # 根据需要采集的内容data_fields
                # 将真实参数记录中的信息添加到voc样本的参数记录中
                for k, v in gt_record.items():
                    if k in self.data_fields:
                        voc_record[k] = v
                
                # 检查当前处理的样本中是否包含目标
                if len(objs) == 0: # 不包含，当作空样本
                    empty_records.append(voc_record)
                else: # 包含则为有效样本
                    records.append(voc_record)
                
                # 当前样本处理完成，样本计数+1
                # 表示当前处理了多少个样本，
                # 同时也是下一个样本的图片id
                count += 1
                # 达到采样数量及时退出数据的采样解析
                if self.sample_num > 0 and count >= self.sample_num:
                    break
            
            # 检查整个数据集是否为空
            if count == 0:
                try:
                    raise AssertionError()
                except:
                    error_traceback(logger=logger,
                                    lasterrorline_offset=6,
                                    num_lines=3)
                    logger.error("Summary: the count should be more than 0. This means hasn't any sample.")
                    sys.exit(1)
            logger.info("Parsing {0} sample.".format(count) + \
                "\n\t\tSample with targets: {0}.".format(len(records)) + \
                "\n\t\tSample without targets: {0}.".format(len(empty_records)))

            # 处理空样本
            if self.allow_empty and len(empty_records) > 0:
                # 采样空样本
                empty_records = self._sample_empty(empty_records, count)
                records += empty_records
            logger.info("Finished collect {0} sample to use.".format(len(records)))

            # 遍历样本并重置图片id
            for idx, _record in enumerate(records):
                _record['im_id'] = idx
            self.samples = records
            self.cls2id = cls2id
            self.length = len(self.samples)
            logger.info("Finished to parse VOC Dataset cost: {0:.2f}s.".format(
                time.time() - start_time))

    def get_cls2id(self) -> Dict[str, int]:
        """获取解析数据集后得到的类别到id的映射字典
            desc:
                Parameters:
                    None
                Returns:
                    (Dict[str, int])类别到id映射字典
        """
        if self.samples:
            return self.cls2id
        return None


