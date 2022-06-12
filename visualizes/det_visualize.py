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
# includes: det_visualize functions
import os
import sys
import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt

from typing import Dict, Union, Sequence
from loggers import create_logger, error_traceback
logger = create_logger(logger_name='det_visualize')

__all__ = ['visualize_img', 'visualize_bbox', 'visualize_det', 'colormap']


def colormap(rgb: bool=False) -> np.ndarray:
    """获取可视化需要的颜色表
        desc(描述):
            Parameters:
                rgb: 图像是否为rgb格式(bool)
            Returns:
                色彩表
    Get colormap
    The code of this function is copied from https://github.com/facebookresearch/Detectron/blob/main/detectron/utils/colormap.py
    """
    color_list = np.array([
        0.000, 0.447, 0.741, 0.850, 0.325, 0.098, 0.929, 0.694, 0.125, 0.494,
        0.184, 0.556, 0.466, 0.674, 0.188, 0.301, 0.745, 0.933, 0.635, 0.078,
        0.184, 0.300, 0.300, 0.300, 0.600, 0.600, 0.600, 1.000, 0.000, 0.000,
        1.000, 0.500, 0.000, 0.749, 0.749, 0.000, 0.000, 1.000, 0.000, 0.000,
        0.000, 1.000, 0.667, 0.000, 1.000, 0.333, 0.333, 0.000, 0.333, 0.667,
        0.000, 0.333, 1.000, 0.000, 0.667, 0.333, 0.000, 0.667, 0.667, 0.000,
        0.667, 1.000, 0.000, 1.000, 0.333, 0.000, 1.000, 0.667, 0.000, 1.000,
        1.000, 0.000, 0.000, 0.333, 0.500, 0.000, 0.667, 0.500, 0.000, 1.000,
        0.500, 0.333, 0.000, 0.500, 0.333, 0.333, 0.500, 0.333, 0.667, 0.500,
        0.333, 1.000, 0.500, 0.667, 0.000, 0.500, 0.667, 0.333, 0.500, 0.667,
        0.667, 0.500, 0.667, 1.000, 0.500, 1.000, 0.000, 0.500, 1.000, 0.333,
        0.500, 1.000, 0.667, 0.500, 1.000, 1.000, 0.500, 0.000, 0.333, 1.000,
        0.000, 0.667, 1.000, 0.000, 1.000, 1.000, 0.333, 0.000, 1.000, 0.333,
        0.333, 1.000, 0.333, 0.667, 1.000, 0.333, 1.000, 1.000, 0.667, 0.000,
        1.000, 0.667, 0.333, 1.000, 0.667, 0.667, 1.000, 0.667, 1.000, 1.000,
        1.000, 0.000, 1.000, 1.000, 0.333, 1.000, 1.000, 0.667, 1.000, 0.167,
        0.000, 0.000, 0.333, 0.000, 0.000, 0.500, 0.000, 0.000, 0.667, 0.000,
        0.000, 0.833, 0.000, 0.000, 1.000, 0.000, 0.000, 0.000, 0.167, 0.000,
        0.000, 0.333, 0.000, 0.000, 0.500, 0.000, 0.000, 0.667, 0.000, 0.000,
        0.833, 0.000, 0.000, 1.000, 0.000, 0.000, 0.000, 0.167, 0.000, 0.000,
        0.333, 0.000, 0.000, 0.500, 0.000, 0.000, 0.667, 0.000, 0.000, 0.833,
        0.000, 0.000, 1.000, 0.000, 0.000, 0.000, 0.143, 0.143, 0.143, 0.286,
        0.286, 0.286, 0.429, 0.429, 0.429, 0.571, 0.571, 0.571, 0.714, 0.714,
        0.714, 0.857, 0.857, 0.857, 1.000, 1.000, 1.000
    ]).astype(np.float32)
    color_list = color_list.reshape((-1, 3)) * 255
    if not rgb:
        color_list = color_list[:, ::-1]
    return color_list

# 还未替换日志输出，仍然为标准输出
def visualize_img(img: Union[np.ndarray, str],
                  save_path: Union[None, str]=None,
                  show_img: bool=False,
                  is_rgb: bool=False) -> None:
    """利用pyplot可视化图像
        desc(描述):
            Parameters:
                img: 要显示图像的数据(numpy.ndarray)或要显示图像的路径(str)
                save_path: None或可视化结果图像的保存路径(str)
                           如果为None，则不保存
                show_img: 是否使用pyplot显示可视化结果(bool)
                is_rgb: 是否为RGB格式的图像数据，保证图像显示和保存时的色域正确
            Returns:
                None
    """
    if isinstance(img, str): # 为图像路径时
        if os.path.exists(img): # 路径存在
            img = Image.open(img) # 读取图像 -- rgb格式/gray格式
            is_rgb = True
        else: # 不存在的路径，抛出值异常
            try:
                raise ValueError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=9,
                                num_lines=6)
                logger.error('Summary: The img path does not exist.(path: {0})'.format(
                    img))
                sys.exit(1)
        img=np.array(img).astype('uint8') # 转换为numpy.ndarray数组数据-dtype为uint8
    elif isinstance(img, np.ndarray): # 为运行的图像数据
        img=img.astype('uint8') # 转换dtype为uint8
    else: # img参数类型异常，抛出类型异常
        try:
            raise ValueError()
        except:
            error_traceback(logger=logger,
                            lasterrorline_offset=22,
                            num_lines=19)
            logger.error('Summary: The img only support numpy.ndarray or str.(type: {0})'.format(
                type(img)))
            sys.exit(1)
    
    # 至少有一种可视化指令打开
    if show_img==False and save_path is None:
        try:
            raise ValueError()
        except:
            error_traceback(logger=logger,
                            lasterrorline_offset=6,
                            num_lines=3)
            logger.error('Summary: The function of visualize should open the show_img or enter the save_path.')
            sys.exit(1)
    
    if show_img:
        if is_rgb == False: # 输入图像数据为BGR格式
            # 三通道图像时，则将opencv的BGR转为RGB格式
            if len(img.shape)==3 and img.shape[2]==3:
                img = img[:, :, ::-1]
        # 可视化窗口显示图像
        plt.figure("visualize result") # 图像窗口命令
        plt.imshow(img) # 显示图像
        plt.axis("off") # 关闭坐标轴显示
        plt.title("result") # 图像标题
        plt.show() # 显示图像

    # 保存可视化图像
    if save_path: # 路径不为None
        if is_rgb == True: # 图像格式为RGB
            # 三通道图像时，则将RGB格式转为opencv的BGR格式
            if len(img.shape)==3 and img.shape[2]==3:
                img = img[:, :, ::-1]
        try: # 尝试保存图像
            cv2.imwrite(save_path, img)
            logger.info("The visualize result has save at: {0}.".format(save_path))
        except :
            logger.warning("The save_path is not a file.({0})".format(save_path))

def visualize_bbox(bboxs: np.ndarray,
                   draw_board: np.ndarray,
                   score_threshold: float=0.5,
                   labels: Union[Sequence[str], Dict[int, str]]=None,
                   use_rgb: bool=False) -> np.ndarray:
    """可视化bbox
        desc(描述):
            Parameters:
                bboxs: 要显示边界框的数据(numpy.ndarray)
                       shape: [N, 4] or [N, 6]
                       [0, 4] --> x1, y1, x2, y2
                       [0, 6] --> class, score, x1, y1, x2, y2
                draw_board: 画板背景图像(numpy.ndarray)或要显示图像的路径(str)
                score_threshold: 检测可视化输出的得分阈值(float)，小于该值的
                                 边界框不可视化
                                 value: [0., 1.)
                lables: 类别ID对应的类别名称(list|tuple|set|dict[int, str])
                use_rgb: 背景图像格式是否为rgb格式(bool)
            Returns:
                将边界框(当输入bboxs的shape为[N, 6]时包含类别)可视化
                后的图像(numpy.ndarray)
                shape: 与draw_board一致
    """
    # 判断bboxs是否含有类别与得分:
    # len(bboxs[0]) == 4，说明不包含
    include_cls = False if len(bboxs[0]) == 4 else True

    # 图像获取
    if isinstance(draw_board, str): # 为图像路径时
        if os.path.exists(draw_board): # 路径存在
            draw_board=Image.open(draw_board) # 读取图像
            use_rgb=True # PIL.Image读取的图像格式为RGB
        else: # 不存在的路径，抛出值异常
            try:
                raise ValueError()
            except:
                error_traceback(logger=logger,
                                lasterrorline_offset=10,
                                num_lines=7)
                logger.error('The draw_board path does not exist.(path: {0})'.format(
                    draw_board))
                sys.exit(1)
        draw_board=np.array(draw_board).astype('uint8') # 转换为numpy.ndarray数组数据-dtype为uint8
    elif isinstance(draw_board, np.ndarray): # 为运行的图像数据
        draw_board=draw_board.astype('uint8') # 转换dtype为uint8
    else: # img类型异常，抛出类型异常
        try:
            raise ValueError()
        except:
            error_traceback(logger=logger,
                            lasterrorline_offset=23,
                            num_lines=20)
            logger.error('The img only support numpy.ndarray or str.(type: {0})'.format(
                type(draw_board)))
            sys.exit(1)

    # 图像通道检查: 由于colormap为三通道的，所以强制所有可视化为三通道
    if len(draw_board.shape) == 2: # 单通道图像的处理方式
        draw_board = np.stack([draw_board]*3, axis=-1)
    elif len(draw_board.shape) == 3 and draw_board.shape[2] >= 4: # 多通道图像的处理方式
        draw_board = draw_board[:, :, :3]
    
    # 图像大小获取
    h, w, _ = draw_board.shape # 高、宽
    # 绘制参数控制
    scale_size = 512 # 字体以及线条大小缩放因子
    font_scale = max(min(max(h, w) / scale_size, 0.8), 0.5) # 字体scale
    font_thickness = int((max(h, w) / scale_size + 1) * 1.0) # 字体大小
    font_y_offset = font_thickness * 2 # 字体显示向上偏移一定像素
    rectangle_thickness = int((max(h, w) / scale_size + 1) * 1.0) # 线条大小

    # 获取颜色表
    _color_map = colormap(rgb=use_rgb)
    
    for idx, box in enumerate(bboxs): # 遍历每一个边界框并绘制
        # 类比id
        cls_id =  box[0].item() if include_cls else None
        # 类别得分
        score = box[1].item() if include_cls else None
        if score is not None and score < score_threshold: # 跳过不满足的bbox
            continue
        # 边界框
        bbox = box[2:] if include_cls else box
        # 绘制颜色
        _color = _color_map[int(cls_id)%80] if include_cls else _color_map[0]
        _color = tuple(int(i) for i in _color)
        
        # 绘制边界框
        cv2.rectangle(draw_board, [int(bbox[0]), int(bbox[1])], [int(bbox[2]), int(bbox[3])],
                      color=_color, thickness=rectangle_thickness)
        
        # 绘制类别描述: class_name + score
        if cls_id is not None: # 存在类别信息时
            # 可视化class_name的预处理
            # lables为None时直接使用class_id进行可视化
            cls_name = labels[int(cls_id)] + '-' + str(round(score, 2)) if \
                       labels is not None else str(int(cls_id)) + '-' + str(round(score, 2))
            cv2.putText(draw_board, cls_name,
                        (int(bbox[0]), int(bbox[1])-font_y_offset), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=font_scale, color=_color, thickness=font_thickness)

    return draw_board, use_rgb

def visualize_det(img, cls_and_bboxs,
                  score_threshold: float=0.5,
                  save_path: Union[None, str]=None,
                  labels: Union[Sequence[str], Dict[int, str]]=None,
                  use_rgb: bool=False,
                  show_img: bool=False) -> np.ndarray:
    """可视化检测模型的输出结果
        desc(描述):
            Parameters:
                img: 检测输入图像的数据(numpy.ndarray)或检测输入图像的路径(str)
                cls_and_bboxs: 检测输出边界框与对应类别的数据(numpy.ndarray)
                               shape: [N, 6]
                               [0, 6] --> class, score, x1, y1, x2, y2
                score_threshold: 检测可视化输出的得分阈值(float)，小于该值的
                                 边界框不可视化
                                 value: [0., 1.)
                save_path: None或可视化结果图像的保存路径(str)
                           如果为None，则不保存
                lables: 类别ID对应的类别名称(list|tuple|set|dict[int, str])
                use_rgb: 背景图像格式是否为rgb格式(bool)
                show_img: 是否使用pyplot显示可视化结果(bool)
            Returns:
                将边界框与类别可视化后的图像(numpy.ndarray)
                shape: 与输入真实图像一致
    """
    # 可视化bbox到目标图像
    visualize_result, _is_rgb = visualize_bbox(bboxs=cls_and_bboxs,
                                                draw_board=img,
                                                score_threshold=score_threshold,
                                                labels=labels,
                                                use_rgb=use_rgb)

    # 可视化窗口展示与可视化结果图像保存
    visualize_img(visualize_result, save_path=save_path, show_img=show_img, is_rgb=_is_rgb)

    # 返回后续可能会用上的可视化结果
    return visualize_result