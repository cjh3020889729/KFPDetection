# 可视化接口实现说明

> Start Date: 2022.5.19
> 
> 修订次数: 1
> 
> End Date: 2022.5.19

分别设计图像显示与保存、边界框绘制、外部检测可视化接口实现检测模型中常用的可视化支持。

目录结构:
```
    |- __init__.py
    |- det_visualize.py
```

接口分布:
```
    |- det_visualize.py
        functions:
        |- colormap
        |- visualize_img
        |- visualize_bbox
        |- visualize_det
```

1. 对于图像显示与保存(det_visualize.py):
    - 接口类型: 函数(visualize_img)
    - 函数用途:
        - 作为所有可视化接口需要保存与显示结果的落脚点
    - 输入参数:
        - img: 图像数据/路径
        - save_path: 保存可视化图像的路径或None
        - show_img: 是否使用pyplot显示可视化图像
    - 返回参数:
        - None(无)
    - 函数解读:
        - 输入参数方面:
            - (img)为了展示图像，因此需要传入图像数据；同时支持图像路径的读取方式
            - (save_path)在模型输出可视化中，往往需要对可视化结果进行保存，因此允许启用该参数进行保存路径的配置；且该参数应为具体的图片(文件)路径
            - (show_img)在模型可视化时，除了保存的方式另行查看可视化图像外，还应该支持实时查看；该参数会 用pyplot进行图像显示
        - 返回参数方面:
            - (None)该函数面向实时显示与保存可视化结果，因此无需返回任何结果

2. 对于边界框绘制(det_visualize.py):
    - 接口类型: 函数(visualize_bbox)
    - 函数用途:
        - 将边界框绘制到目标图像上，并将绘制结果返回
        - 返回的结果可以用于各种处理，包括visualize_img的显示与保存
    - 输入参数:
        - bboxs: 边界框数据

            数据最后一维度的大小为4时，表示:x1,y1,x2,y2

            数据最后一维度的大小为6时，表示:cls,score,x1,y1,x2,y2

        - draw_board: 目标图像数据/目标图像路径
        - score_threshold: 边界框可视化绘制阈值

            低于阈值不会绘制

        - lables: 类别id与类别name的映射，可以是序列或字典[id->str]
        - use_rgb: 表示输入数据是不是rgb格式

            opencv读取的数据为bgr格式，则此处为False

            PIL读取的数据为rgb格式，则此处为True

            特别地，当draw_board为路径时，use_rgb设置无效，

            会强制为True——因为内部读取图像采用PIL.Image

    - 返回参数:
        - numpy.ndarray: 与输入目标图像等大的可视化结果
    - 函数解读
        - 输入参数方面:
            - (bboxs)目的是展示需要可视化的边界框，但是考虑模型输出可视化与数据预处理可视化两方面；
                
                因此，支持两种格式的输入——维度大小为4对应数据预处理，另外指向模型输出可视化

            - (draw_board)绘制边界框需要背景图像，因此传入目标图像数据作为背景进行可视化；
                
                同时支持图像路径的读取方式

            - (score_threshold)为了控制边界框的可视化，通过阈值来剔除不合格的边界框
            - (lables)在边界框包含类别id时，允许将可视化的类别id换为类别name(lables不为None)
                
                lables为None，则可视化保持str(id)进行可视化

            - (use_rgb)用于控制colormap中的色彩值顺序——rgb与bgr格式图像数据的colormap中单个类别颜色
                
                向量的元素值是倒序的

        - 返回参数方面:
            - (numpy.ndarray)保证与输入目标图像等大的可视化结果，可用于其它处理/visualize_img可视化

3. 对于边界框绘制(det_visualize.py):
    - 接口类型: 函数(visualize_det)
    - 函数用途:
        - 可视化检测模型的输出结果
    - 输入参数:
        - img: 可视化结果需要的目标图像；
            
            同时支持图像路径的读取方式

        - cls_and_bboxs: 目的是对检测模型输出数据的可视化
            
            最后一维度大小为6——cls,score,x1,y1,x2,y2

        - score_threshold: 为了控制边界框的可视化，通过阈值来剔除不合格的边界框
        - save_path: 在模型输出可视化中，往往需要对可视化结果进行保存，因此允许启用该参数进行保存路径
            
            的配置；且该参数应为具体的图片(文件)路径

        - lables: 在边界框包含类别id时，允许将可视化的类别id换为类别name(lables不为None)

            lables为None，则可视化保持str(id)进行可视化

        - use_rgb: 用于控制colormap中的色彩值顺序——rgb与bgr格式图像数据的colormap中单个类别颜色
           
            向量的元素值是倒序的

        - show_img: 在模型可视化时，除了保存的方式另行查看可视化图像外，还应该支持实时查看；该参数会 
                
            用pyplot进行图像显示

    - 返回参数:
        - numpy.ndarray: 返回可视化结果，方便支持其它需要的图像操作
    - 函数解读
        - 输入参数方面:
            - (前述充分，不再补充)
        - 返回参数方面:
            - (前述充分，不再补充)

4. 对于颜色表(det_visualize.py):
    - 接口类型: 函数(colormap)
    - 来源: https://github.com/facebookresearch/Detectron/blob/main/detectron/utils/colormap.py
    - 函数用途:
        - 实现可视化不同类别所需的颜色向量(R, G, B)
        - 默认颜色向量值对应BGR(use_rgb=False)，即opencv读取图像的色值
    - 输入参数:
        - use_rgb: 根据可视化检测结果/边界框时的目标图像数据格式设置
            
            当use_rgb为False，产生的colormap适合opencv读取的图像格式BGR

            反之，适合像PIL读取的RGB格式图像

    - 返回参数:
        - numpy.ndarray: 返回根据图像格式调整的colormap
    - 函数解读
        - 输入参数方面:
            - (use_rgb)由于图像读取的方式很多，不同的方式读取的数据格式存在不同
                
                因此，针对主流的RGB格式与BGR格式进行区分对待

        - 返回参数方面:
            - (colormap)可以实现不同类别用不同颜色进行展示
                
                只支持79种不同的颜色

                为了任意类别的显示，可以使用colormap[int(cls_id)%80]来循环设定
                
