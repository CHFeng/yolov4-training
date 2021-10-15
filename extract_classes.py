import os

from shutil import copyfile
from pycocotools.coco import COCO
from xml.dom.minidom import parseString
from lxml.etree import Element, SubElement, tostring
from IPython.display import clear_output
# for parse command line
from absl import app, flags, logging
from absl.flags import FLAGS

pwd = os.path.abspath(os.getcwd())
flags.DEFINE_string("source_path", pwd, "coco圖片集的路徑")
flags.DEFINE_string("output_path", pwd + "/extracted_dataset/", "抽取出的圖片集存放路徑")
flags.DEFINE_string("class_list", "person,car", "設定要抽取出的圖片集類別")


def update_progress(progress):
    bar_length = 20
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1
    block = int(round(bar_length * progress))
    clear_output(wait=True)
    text = "Progress: [{0}] {1:.1f}%".format("#" * block + "-" * (bar_length - block), progress * 100)
    print(text)


def main(argv):
    # define the path of source image and annotations
    COCO_ANNOTATIONS_PATH = FLAGS.source_path + "/annotations/instances_train2017.json"
    COCO_IMAGES_DIRECTORY = FLAGS.source_path + "/train2017/"
    OUTPUT_FOLDER_NAME = FLAGS.output_path.split('/')[len(FLAGS.output_path.split('/')) - 2]
    # create output folder
    if not os.path.exists(FLAGS.output_path):
        os.mkdir(FLAGS.output_path)
    # load coco dataset
    coco = COCO(COCO_ANNOTATIONS_PATH)

    # list all classes of coco dataset
    # cats = coco.loadCats(coco.getCatIds())
    # nms = [cat['name'] for cat in cats]
    # print(nms)

    # set target classes that we want
    target_classes = FLAGS.class_list.split(',')
    img_dict = {}
    for classes in target_classes:
        catIds = coco.getCatIds(catNms=[classes])
        imgIds = coco.getImgIds(catIds=catIds)
        for imgID in imgIds:
            try:
                content = ''
                content = img_dict[imgID] + ','
            except:
                pass
            img_dict[imgID] = content + classes

    total_progress = len(img_dict)
    progress = 0

    for img_id in img_dict:
        progress += 1
        annotation_ids = coco.getAnnIds(img_id)
        annotations = coco.loadAnns(annotation_ids)

        image_meta = coco.loadImgs(annotations[0]["image_id"])[0]
        node_root = Element('annotation')
        node_folder = SubElement(node_root, 'folder')
        node_folder.text = OUTPUT_FOLDER_NAME
        node_filename = SubElement(node_root, 'filename')
        node_filename.text = image_meta['file_name']
        node_size = SubElement(node_root, 'size')
        node_width = SubElement(node_size, 'width')
        node_width.text = str(image_meta['width'])
        node_height = SubElement(node_size, 'height')
        node_height.text = str(image_meta['height'])
        node_depth = SubElement(node_size, 'depth')
        node_depth.text = '3'

        for i in range(len(annotations)):
            entity_id = annotations[i]["category_id"]
            entity = coco.loadCats(entity_id)[0]["name"]
            if entity in target_classes:
                node_object = SubElement(node_root, 'object')
                node_name = SubElement(node_object, 'name')
                node_name.text = entity
                node_difficult = SubElement(node_object, 'difficult')
                node_difficult.text = '0'
                node_bndbox = SubElement(node_object, 'bndbox')
                node_xmin = SubElement(node_bndbox, 'xmin')
                node_xmin.text = str(round(annotations[i]['bbox'][0]))
                node_ymin = SubElement(node_bndbox, 'ymin')
                node_ymin.text = str(round(annotations[i]['bbox'][1]))
                node_xmax = SubElement(node_bndbox, 'xmax')
                node_xmax.text = str(round(annotations[i]['bbox'][0] + annotations[i]['bbox'][2]))
                node_ymax = SubElement(node_bndbox, 'ymax')
                node_ymax.text = str(round(annotations[i]['bbox'][1] + annotations[i]['bbox'][3]))

        xml = tostring(node_root, pretty_print=True)
        dom = parseString(xml)
        with open(FLAGS.output_path + image_meta['file_name'].split('.')[0] + '.xml', 'w') as xml_file:
            xml_file.write(dom.toxml())

        copyfile(COCO_IMAGES_DIRECTORY + image_meta['file_name'], FLAGS.output_path + image_meta['file_name'])
        update_progress(progress / total_progress)


if __name__ == "__main__":
    try:
        app.run(main)
    except SystemExit:
        pass