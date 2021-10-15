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
安裝相關套件
```
pip install pycoco
pip install lxml
pip install IPython
```

執行extract_classes.py，指定參數如下：

* source_path: coco圖片集的路徑
* output_path: 存放抽取出的圖片路徑
* class_list: 設定要抽取出的圖片集類別
```
python extract_classes.py -source_path the/source/path -output_path the/output/path -class_list person,car,motorcycle,bus,truck
```

## 將XML標記轉換為YOLO格式
[標記圖檔格式說明](https://towardsdatascience.com/image-data-labelling-and-annotation-everything-you-need-to-know-86ede6c684b1)

yolo使用.txt來讀取要訓練用的標記格式，因此我們需要將xml轉換成yolo使用的格式。

Pascal VOC xml格式如下：
```
<annotation>
	<folder>images</folder>
	<filename>{FILENAME}</filename>
	<path>{PATH}</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>{WIDTH}</width>
		<height>{HEIGHT}</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
    <object>
		<name>{NAME}</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>{XMIN}</xmin>
			<ymin>{YMIN}</ymin>
			<xmax>{XMAX}</xmax>
			<ymax>{YMAX}</ymax>
		</bndbox>
	</object>
</annotation>
```
YOLO格式如下：
```
<object-class> <x> <y> <width> <height>
```
執行xmlTotxt.py，指定參數如下：

* source_path: coco圖片集的路徑
* output_path: yolo .txt檔案的存放路徑
* class_list: 設定要轉換的圖片集類別