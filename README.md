# yolov4-training
使用darknet進行機器訓練偵測模型

## 準備圖片素材
圖片來源

* [COCO](https://cocodataset.org/#download)

* [PASCAL VOC](https://cv.gluon.ai/build/examples_datasets/pascal_voc.html)

這邊以COCO為例，下載2017 Train images[18G] & 2017 Train/Val annotations [241MB]，並解壓縮。
```bash
    # create folder
    mkdir coco_dataset
    # download annotations
    wget http://images.cocodataset.org/annotations/
    annotations_trainval2017.zip
    # download pictures
    wget http://images.cocodataset.org/zips/train2017.zip
    # unzip
    unzip train2017.zip
    unzip annotations_trainval2017.zip
```
## 從COCO圖片集中抽取目標類別圖片
因coco dataset具有90個類別圖片集，我們只需要抽取我們想要訓練的圖片集即可。
執行extract_classes.py，指定參數如下：

* source_path: coco圖片集的路徑
* output_path: 存放抽取出的圖片路徑
* class_list: 設定要抽取出的圖片集類別
```
python extract_classes.py -source_path the/source/path -output_path the/output/path -class_list person,car,motorcycle,bus,truck
```