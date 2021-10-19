import random
import os
from shutil import copyfile
# for parse command line
from absl import app, flags
from absl.flags import FLAGS

pwd = os.path.abspath(os.getcwd())
flags.DEFINE_string("img_path", pwd, "要訓練圖片的路徑")
flags.DEFINE_string("cfg_path", os.path.join(pwd, "yolo_cfg"), "存放yolo config的路徑")
flags.DEFINE_integer("total_classes", 6, "總共有幾個類別要訓練")
flags.DEFINE_bool("tiny", False, "是否使用tiny版本的yolov4 config")
TEST_RATIO = 0.2


def main(argv):
    fileList = []
    outputTrainFile = os.path.join(FLAGS.cfg_path, "train.txt")
    outputTestFile = os.path.join(FLAGS.cfg_path, "test.txt")
    # make sure the yolo config folder existed
    if not os.path.exists(FLAGS.cfg_path):
        os.makedirs(FLAGS.cfg_path)
    # collect all images from image folder
    for file in os.listdir(FLAGS.img_path):
        filename, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()

        if (file_extension == ".jpg" or file_extension == ".jpeg" or file_extension == ".png" or file_extension == ".bmp"):
            fileList.append(os.path.join(FLAGS.img_path, file))
    # calculate the number for testing
    testCount = int(len(fileList) * TEST_RATIO)
    trainCount = len(fileList) - testCount
    print("Total images:{} train images:{} test images:{}".format(len(fileList), trainCount, testCount))
    # random split source images into train and test
    a = range(len(fileList))
    test_data = random.sample(a, testCount)
    train_data = [x for x in a if x not in test_data]
    # write file list for training into train.txt
    with open(outputTrainFile, 'w') as the_file:
        for i in train_data:
            the_file.write(fileList[i] + "\n")
    the_file.close()
    # write file list for testing into test.txt
    with open(outputTestFile, 'w') as the_file:
        for i in test_data:
            the_file.write(fileList[i] + "\n")
    the_file.close()
    # create weights folder
    weights_path = os.path.join(FLAGS.cfg_path, "weights")
    if not os.path.exists(weights_path):
        os.makedirs(weights_path)
        print("all weights will generated in here: ", weights_path)
    # write yolo train config
    with open(os.path.join(FLAGS.cfg_path, "obj.data"), 'w') as the_file:
        the_file.write("classes= " + str(FLAGS.total_classes) + "\n")
        the_file.write("train  = " + os.path.join(FLAGS.cfg_path, "train.txt") + "\n")
        the_file.write("valid  = " + os.path.join(FLAGS.cfg_path, "test.txt") + "\n")
        the_file.write("names = " + os.path.join(FLAGS.cfg_path, "obj.names") + "\n")
        the_file.write("backup = " + os.path.join(FLAGS.cfg_path, "weights") + "/")
    the_file.close()
    # copy obj.name into config folder
    copyfile(os.path.join(FLAGS.img_path, "obj.names"), os.path.join(FLAGS.cfg_path, "obj.names"))
    # create config file base on yolov4
    numBatch = 64
    numSubdivision = 16
    filterNum = (FLAGS.total_classes + 5) * 3
    if (FLAGS.tiny):
        yolo_cfg_name = "yolov4-tiny.cfg"
    else:
        yolo_cfg_name = "yolov4.cfg"

    with open(os.path.join("yolov4-orig-cfg", yolo_cfg_name)) as file:
        file_content = file.read()
    file.close
    batch = "batch = " + str(numBatch)
    subdivision = "subdivisions = " + str(numSubdivision)
    # the max batches = classes*2000, but not less than number of training images and not less than 6000
    val = FLAGS.total_classes * 2000
    if val < trainCount:
        val = (int(trainCount / 1000) + 1) * 1000
    if val < 6000:
        val = 6000
    max_batches = "max_batches = " + str(val)
    steps = "steps = " + str(int(val * 0.8)) + "," + str(int(val * 0.9))
    filter = "filters = " + str(filterNum)
    classes = "classes = " + str(FLAGS.total_classes)
    # read anchors value from file
    with open("anchors.txt") as file:
        anchorStr = file.read()
        anchorStr = "anchors = " + anchorStr
    file.close
    # according our resource to modify the yolo config file
    file_updated = file_content.replace("batch = input batch number", batch)
    file_updated = file_updated.replace("subdivisions = input subdivisions number", subdivision)
    file_updated = file_updated.replace("max_batches = input max batches", max_batches)
    file_updated = file_updated.replace("steps = input steps", steps)
    file_updated = file_updated.replace("filters = input filters", filter)
    file_updated = file_updated.replace("classes = input classes", classes)
    file_updated = file_updated.replace("anchors = input anchors", anchorStr)

    file = open(os.path.join(FLAGS.cfg_path, yolo_cfg_name), "w")
    file.write(file_updated)
    file.close


if __name__ == "__main__":
    try:
        app.run(main)
    except SystemExit:
        pass