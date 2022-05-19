# KFPDetection检测套件
---
author: Jinghui Cai(红白黑)

qq: 3020889727

weixin: cjh3020889729

---
The Kid From PaddleDetection —— 基于教学的检测平台搭建


> Start Date: 2022.5.18
>
> End Date: ~
>
>
> Package Name: The Kid from PaddleDetection
> 
> Means: 参考PaddleDetection检测套件的一个目标检测平台全流程实现

当前进度: 1.5/12
> over-6.1
> 
> over-7.2
> 
> todo-7.1

- 0.实现数据加载(预处理)
    - 0.1 数据加载(dir at ./datasets): VOC + COCO
    - 0.2 数据预处理(dir at ./transforms): 图像预处理 + 架构输入预处理
- 1.实现模块解耦
    - 1.1 骨干网络(dir at ./backbones): 各类骨干网络
    - 1.2 Neck结构(dir at ./necks): 各类Neck
    - 1.3 Head结构(dir at ./heads): 各类Head
- 2.实现自由组网
    - 2.1 模型架构(dir at ./architectures): 各类检测模型架构
- 3.实现模型参数初始化
    - 3.1 模型处理化(dir at ./initializers): 各种参数初始化器
- 4.实现数据后处理
    - 4.1 输出后处理(dir at ./postprocesses): 各种架构输出的后处理
- 5.实现多种NMS
    - 5.1 对检测结果进行NMS处理(dir at ./nmses): 各种NMS算法
- 6.实现可视化
    - 6.1 可视化输出(dir at ./visualizes): 检测结果可视化与预处理可视化
- 7.实现日志记录
    - 7.1 日志可视化记录(dir at ./vdlrecords): 不同类型数据的日志记录
    - 7.2 运行日志记录/输出(dir at ./loggers): 日志器
- 8.实现模型导出
    - 8.1 模型导出(dir at ./tools): 训练模型的导出
- 9.实现模型量化(TODO)
- 10.实现模型裁剪(TODO)
- 11.实现模型蒸馏(TODO)