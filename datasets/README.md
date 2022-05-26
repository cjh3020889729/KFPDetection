# 数据集相关接口

> Start Date: 2022.5.21
> 
> 修订次数: 1
> 
> End Date: 2022.5.21

分别设计数据集加载基类、VOC数据集加载、COCO数据集加载、数据集生成和转换以及数据集加载器的接口。

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
        functions:
        |- check_img_endswith
        class:
        |- DetDataset
        |- ImageFolder
    |- voc.py
        functions:
        |- generate_Vocdataset_and_Voclable
        class:
        |- VOCDataset
    |-coco.py
        functions:
        |- _generate_coco_records
        |- voc2coco
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

1. 对于(含标签)检测数据集加载基类(det.py):
    - 接口类型: 类(DetDataset)
    - 类用途:
        - 
    - 初始化参数:
        - 
    - 类解读:
        - 

2. 对于(不含标签)检测数据集加载基类(det.py):
    - 接口类型: 类(ImageFolder)
    - 类用途:
        - 
    - 初始化参数:
        - 
    - 类解读:
        - 

3. 对于图片文件后缀检查的函数(det.py):
    - 接口类型: 函数(check_img_endswith)
    - 函数用途:
        - 
    - 初始化参数:
        - 
    - 函数解读:
        - 
