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
from symbol import with_item
import shutil
import json
from xml.etree import ElementTree as ET
import numpy as np

from loggers import create_logger, error_traceback
from .voc import check_img_endswith
from typing import Union, Dict, List, Any
logger = create_logger(logger_name=__name__)

__all__ = ['voc2coco']


def _generate_coco_records(anno_list: List[Any],
                           lable_list: List[int]) -> Dict[str, 
                            List[Dict[str, Any]]]:
    """生成coco的dict记录格式
    """
    # 基本信息汇总
    coco_records = {
        'info': {
            'year': 2022,
            'version': 0.1,
            'description': 'from voc2coco',
            'contributor': 'Jinghui Cai',
            'url': 'https://github.com/cjh3020889729/KFPDetection',
            'date_created': '2022-05-23 11:27:39'
        }
    }

    # 图片信息汇总
    _images = [
        {
            'id': idx,
            'width': size[0],
            'height': size[1],
            'file_name': img_name
        } for idx, img_name, size, _ in anno_list
    ]
    coco_records['image'] = _images

    # 标注信息汇总
    _annotations = []
    for anno in anno_list:
        im_id, _, size, bboxs = anno
        for bbox in bboxs:
            box_id, box = bbox
            cls_name, x1, y1, x2, y2 = box
            _annotations.append({
                'id': box_id,
                'image_id': im_id,
                'category_id': lable_list.index(cls_name),
                'segmentation': [],
                'area':(x2-x1) * (y2-y1),
                'bbox':[x1, y1, x2, y2],
                'iscrowd':0
            })
    coco_records['annotations'] = _annotations

    # 类别信息汇总
    _categories = [
        {
            'id': idx,
            'name': _class,
            'supercategory': 'object'
        } for idx, _class in enumerate(lable_list)
    ]
    coco_records['categories'] = _categories
    return coco_records


def voc2coco(image_dir: str,
             anno_dir: str,
             train_ratio: float=0.7,
             output: str=None) -> None:
    """将voc数据转为coco数据
    """
    if output == None or output == '':
        try:
            raise ValueError()
        except:
            error_traceback(logger=logger,
                            lasterrorline_offset=6,
                            num_lines=1)
            logger.error("Summary: The output should be a existed path,"
                " but now it's None or ''.")
            sys.exit(1)

    import time
    start_time = time.time()
    logger.info("Starting VOC2COCO work.")
    logger.info("Starting collect VOC Dataset dir.")

    # 1.解析处理的样本集: [[id, img, xml]...]
    records = []
    img_count = 0
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
                    records.append([img_count, img, anno])
                    anno_files.pop(idx)
                    img_count += 1
                    break
        break

    # 2.生成目标目录
    if not os.path.isdir(output): # 目录不存在
        os.makedirs(output)
    dist_image_dir = os.path.join(os.path.join(output, 'COCODataset'), 'JPEGImages')
    if not os.path.isdir(dist_image_dir):
        os.makedirs(dist_image_dir)
    
    # 3.拷贝文件到目标目录，同时记录样本信息
    logger.info("Start copy source file to dist dataset dir.")
    lable_list = set() # 所有样本的类别
    dist_anno_list = [] # 所有样本的路径信息
    for idx, record in enumerate(records):
        # 读取前期的样本记录
        img, anno = record[1], record[2]
        # 生成完整的图片源文件路径与目标路径
        img_origin = os.path.join(image_dir, img)
        img_dist = os.path.join(dist_image_dir, img)
        # 完成文件拷贝
        shutil.copyfile(img_origin, img_dist)

        # 获取xml路径与标注数据
        anno_path = os.path.join(anno_dir, anno)
        # 读取xml标注文件，收集class/lable +  objs情况
        tree = ET.parse(anno_path)
        if not tree.find('size'):
            logger.warning("The xml file: {0} hasn't size element.".format(anno_path))
            dist_anno_list.append([[], []]) # size + objs(+class)
            continue
        im_w = int(tree.find('size').find('width').text)
        im_h = int(tree.find('size').find('height').text)
        objs = tree.findall('object')
        if len(objs) == 0:
            dist_anno_list.append([[im_w, im_h], []]) # size + objs
            continue
        bbox_records = []
        for obj in objs: # 遍历所有目标，获取类名的集合set
            cls_name = obj.find('name').text
            # 获取边界框坐标
            x1 = int(obj.find('bndbox').find('xmin').text)
            y1 = int(obj.find('bndbox').find('ymin').text)
            x2 = int(obj.find('bndbox').find('xmax').text)
            y2 = int(obj.find('bndbox').find('ymax').text)
            # 矫正坐标值
            x1 = max(x1, 0)
            y1 = max(y1, 0)
            x2 = min(im_w - 1, x2)
            y2 = min(im_h - 1, y2)
            if x2 > x1 and y2 > y1:
                bbox_records.append([cls_name, x1, y1, x2, y2])
            else:
                logger.warning("The bbox([{0}, {1}, {2}, {3}])".format(
                    x1, y1, x2, y2) + \
                    " in xml file: {0}".format(anno_path) + \
                    ", it hasn't error.")
            lable_list.add(cls_name)
        dist_anno_list.append([[im_w, im_h], bbox_records]) # size + objs
        if (idx+1) % int(len(records)*0.2) == 0:
            logger.info("Copy/Work source file: {0} / {1}.".format(
                idx + 1, len(records)))
    
    # 归纳图片信息以及标注信息
    logger.info("Start tidy the information of image and annotation.")
    _count = 0
    _bbox_count = 0
    anno_list = []
    lable_list = list(lable_list)
    for idx in range(len(records)):
        _reocrd = records[idx]
        _anno = dist_anno_list[idx]
        if len(_anno[0]) == 0:
            continue
        _bbox = []
        for box in _anno[1][1:]:
            _bbox.append([_bbox_count, box])
            _bbox_count += 1
        anno_list.append([
            _count, # img_id
            _reocrd[1], # img_name
            _anno[0], # size
            _bbox # bboxs: [[bbox_id, [cls_name, x1, y1, x2, y2]]]
        ])
        _count += 1
    
    # 划分数据集
    import random
    random.shuffle(anno_list)
    train_num = min(len(anno_list), int(len(anno_list)*train_ratio))
    train_anno_list = anno_list[:train_num]
    if train_num == len(anno_list):
        eval_anno_list = []
    else:
        eval_anno_list = anno_list[train_num:]
    
    # 生成coco的参数记录格式
    train_coco_records = _generate_coco_records(
                        anno_list=train_anno_list, lable_list=lable_list)
    eval_coco_records = _generate_coco_records(
                        anno_list=eval_anno_list, lable_list=lable_list)

    # 写入coco-json文件
    dist_train_anno_path = os.path.join(os.path.join(output, 'COCODataset'), 'train.json')
    dist_eval_anno_path = os.path.join(os.path.join(output, 'COCODataset'), 'eval.json')
    # dist_train_coco_json = json.dumps(train_coco_records)
    # dist_eval_coco_json = json.dumps(eval_coco_records)
    with open(dist_train_anno_path, 'w') as f:
        json.dump(train_coco_records, f, indent=4)
    logger.info("The convertion has generate {0} samples for Train,".format(
        len(train_coco_records['image'])) + \
        " and has {0} bbox.".format(len(train_coco_records['annotations'])))
    with open(dist_eval_anno_path, 'w') as f:
        json.dump(eval_coco_records, f, indent=4)
    logger.info("The convertion has generate {0} samples for Train,".format(
        len(eval_coco_records['image'])) + \
        " and has {0} bbox.".format(len(eval_coco_records['annotations'])))
    
    logger.info("Total convert {0} sample.".format(len(anno_list)))
    logger.info("Dist COCODataset Dir Tree:\n"
            "|- {0}\n\t|- {1}\n\t\t|- {2}\n\t\t|- {3}\n\t\t|- {4}".format(
            os.path.abspath(output), 'COCODataset',
            'JEPGImages',
            'train.json', 'eval.json'))
    logger.info("Total cost: {0:.2f}s.".format(time.time() - start_time))
