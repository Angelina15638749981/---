import sys
from PIL import Image


def get_top_pixels(file_path, min_pt_num):
    im = Image.open(file_path)
    im = im.convert("P")
    top_pixels = []

    for index in enumerate(im.histogram()):
        if index[1] > int(min_pt_num):
            top_pixels.append(index)

    return sorted(top_pixels, key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    print(get_top_pixels(sys.argv[1], sys.argv[2]))