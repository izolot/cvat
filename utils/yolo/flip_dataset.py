from PIL import Image, ImageOps
import os
import sys

path = sys.argv[1]

if path[-1] != os.path.sep:
    path += os.path.sep


def convert_from_yolo_format(widht_img, height_img, box):
    bbox_w = float(box[3]) * widht_img
    bbox_h = float(box[4]) * height_img
    center_x = float(box[1]) * widht_img
    center_y = float(box[2]) * height_img
    x_1 = int(center_x - (bbox_w / 2))
    y_1 = int(center_y - (bbox_h / 2))
    x_2 = int(center_x + (bbox_w / 2))
    y_2 = int(center_y + (bbox_h / 2))
    return x_1, y_1, x_2, y_2


def convert_to_yolo_format(widht_img, height_img, box):
    dw = 1. / widht_img
    dh = 1. / height_img
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


for filename in os.listdir(path):
    if not os.path.isdir(os.path.join(path, filename)):
        base, extension = os.path.splitext(filename)
        old_name = os.path.join(path, filename)
        new_name = os.path.join(path, base + "_flipped" + extension)

        if extension != ".txt":
            img = Image.open(old_name)
            width = img.size[0]
            height = img.size[1]
            flipped_img = ImageOps.mirror(img)
            flipped_img.save(new_name)
            print(old_name + ' - flipped!')

            with open(path + base + "_flipped" + ".txt", 'w') as w:
                with open(path + base + ".txt", 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        bbox = line.strip('\n').split(' ')
                        if len(bbox) > 1:
                            (x1, y1, x2, y2) = convert_from_yolo_format(width, height, bbox)
                            flipped_bbox = [bbox[0]]
                            x1_f = width - x2
                            x2_f = width - x1
                            flipped_bbox.extend(convert_to_yolo_format(width, height, [x1_f, x2_f, y1, y2]))
                            w.write(' '.join(map(str, flipped_bbox)) + '\n')
