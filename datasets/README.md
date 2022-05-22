# 数据集相关接口

> Start Date: 2022.5.21
> 
> 修订次数: 1
> 
> End Date: 2022.5.21

分别设计图像显示与保存、边界框绘制、外部检测可视化接口实现检测模型中常用的可视化支持。

目录结构:
```
    |- __init__.py
    |- det.py
    |- voc.py
    |- coco.py
    |- reader.py
    |- dataset.py
    |- README.md
```

接口分布:
```
    |- det.py
        class:
        |- DetDataset
        |- ImageFolder
    |- voc.py
        class:
        |- VOCDataset
    |-coco.py
        class:
        |- COCODataset
    |-reader.py
        class:
        |- Compose
        |- BatchCompose
    |-dataset.py
        class:
        |- DetDataLoader
        |- TrainDetDataLoader
        |- EvalDetDataLoader
        |- TestDetDataLoader
```



