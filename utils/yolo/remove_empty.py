import os
import shutil
import sys

if len(sys.argv) < 2:
    print("path to folder with annotation")
    sys.exit()

path = sys.argv[1]

if path[-1] != os.path.sep:
    path += os.path.sep


list_image = []

count = 0
for filename in os.listdir(path):
    with open("train.txt", "w") as f:
        if not os.path.isdir(os.path.join(path, filename)):
            base, extension = os.path.splitext(filename)
            if extension == ".txt":
                if os.path.getsize(path+filename) == 0:
                    meta_file = path + filename
                    os.remove(meta_file)
                    print('{} remove'.format(meta_file))
                    img_file = path + base + ".jpg"
                    os.remove(img_file)
                    print('{} remove'.format(img_file))
                    count += 1
                else:
                    list_image.append(path + base + ".jpg")

print('{} count remove images'.format(count))

with open("train.txt", "a") as train_file:
    for image in list_image:
        train_file.write(image+"\n")
