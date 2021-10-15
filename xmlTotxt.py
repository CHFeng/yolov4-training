import os
import cv2
from shutil import copyfile
from xml.dom import minidom
# for parse command line
from absl import app, flags
from absl.flags import FLAGS

pwd = os.path.abspath(os.getcwd())
flags.DEFINE_string("source_path", pwd, "coco圖片集的路徑")
flags.DEFINE_string("output_path", os.path.join(pwd, "yolo"), "yolo .txt檔案的存放路徑")
flags.DEFINE_string("class_list", "person,car,motorcycle,bus,truck,licence", "設定要轉換的圖片集類別")
# class list index
classList = {}


def transferYolo(xmlFilePath, imgFilePath, fileName):
    # get width & height from image
    img = cv2.imread(imgFilePath)
    imgShape = img.shape
    img_h = imgShape[0]
    img_w = imgShape[1]
    # parse lable detail from xml file
    labelXML = minidom.parse(xmlFilePath)
    labelName = []
    labelXmin = []
    labelYmin = []
    labelXmax = []
    labelYmax = []
    # parse class name
    tmpArrays = labelXML.getElementsByTagName("name")
    for elem in tmpArrays:
        labelName.append(str(elem.firstChild.data))
    # parse xmin
    tmpArrays = labelXML.getElementsByTagName("xmin")
    for elem in tmpArrays:
        labelXmin.append(int(elem.firstChild.data))
    # parse ymin
    tmpArrays = labelXML.getElementsByTagName("ymin")
    for elem in tmpArrays:
        labelYmin.append(int(elem.firstChild.data))
    # parse xmax
    tmpArrays = labelXML.getElementsByTagName("xmax")
    for elem in tmpArrays:
        labelXmax.append(int(elem.firstChild.data))
    # parse ymax
    tmpArrays = labelXML.getElementsByTagName("ymax")
    for elem in tmpArrays:
        labelYmax.append(int(elem.firstChild.data))
    # define yolo txt file path
    yoloFilePath = os.path.join(FLAGS.output_path, fileName + ".txt")
    # write yolo format into file
    with open(yoloFilePath, 'a') as the_file:
        i = 0
        for className in labelName:
            if className in classList:
                classID = classList[className]
                x = (labelXmin[i] + (labelXmax[i] - labelXmin[i]) / 2) * 1.0 / img_w
                y = (labelYmin[i] + (labelYmax[i] - labelYmin[i]) / 2) * 1.0 / img_h
                w = (labelXmax[i] - labelXmin[i]) * 1.0 / img_w
                h = (labelYmax[i] - labelYmin[i]) * 1.0 / img_h

                the_file.write(str(classID) + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n')
                i += 1

    the_file.close()


def main(argv):
    fileCount = 0
    # set class id according class list
    i = 0
    for className in FLAGS.class_list.split(','):
        classList[className] = i
        i += 1
    # make sure the ouput folder existed
    if not os.path.exists(FLAGS.output_path):
        os.makedirs(FLAGS.output_path)
    # get file name & file extension
    for file in os.listdir(FLAGS.source_path):
        fileName, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()
        if file_extension == ".jpg" or file_extension == ".png" or file_extension == ".jpeg" or file_extension == ".bmp":
            imgfilePath = os.path.join(FLAGS.source_path, file)
            xmlfilePath = os.path.join(FLAGS.source_path, fileName + ".xml")

            if os.path.isfile(xmlfilePath):
                transferYolo(xmlfilePath, imgfilePath, fileName)
                copyfile(imgfilePath, os.path.join(FLAGS.output_path, file))
                fileCount += 1
        if fileCount % 1000 == 0:
            print("Processed files count:%d" % fileCount)

    print("Total files are:%d" % fileCount)


if __name__ == "__main__":
    try:
        app.run(main)
    except SystemExit:
        pass