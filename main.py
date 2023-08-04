import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from pylab import *
from config import config
import os
import shutil


def to_fixed(num_оbj, digits=2):
    return float(f"{num_оbj:.{digits}f}")


def render(input_path, output_path, mode):
    im_transpose = array(Image.open(input_path)).transpose()

    x = range(len(im_transpose))
    y = []
    shadows = []

    for i in im_transpose:
        sorted_mas = sort(i)
        min_intensity = float(sorted_mas[0])
        max_intensity = float(sorted_mas[-1])
        average_point = to_fixed((max_intensity + min_intensity) / 2)
        y.append(average_point)
        shadows.append(to_fixed(max_intensity - average_point))

    plt.errorbar(x, y, yerr=shadows, fmt=config["shadows"]["fmt"], ecolor=config["shadows"]["color"],
                 color='#00000000',
                 elinewidth=config["shadows"]["width"], markersize=0)
    plt.plot(x, y, color=config["plot"]["color"], linewidth=config["plot"]["linewidth"])

    ax = plt.axes()
    ax.set(facecolor=config["background"]["color"])
    plt.grid(config["background"]["grid"])
    plt.xticks([])
    plt.yticks([])

    if mode == "slider":
        plt.show()
    elif mode == "saver":
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()


def scan_dirs(path=config["input_path"]):
    for f in os.scandir(path):
        if f.is_file():
            file_name = f.path.split('\\')[-1].split('.')[0]+'.png'
            inp = f.path.split('\\')[-2]
            if not os.path.exists(config["output_path"] + '\\' + inp):
                os.mkdir(config["output_path"] + '\\' + inp)
            render(f.path, config["output_path"] + '\\' + inp + '\\' + file_name, "saver")
        else:
            scan_dirs(f.path)


if os.path.isfile(config["input_path"]):
    render(config["input_path"], config["output_path"], config["mode"])
else:
    if not os.path.exists(config["output_path"]):
        os.mkdir(config["output_path"])
    else:
        if config["output_autoclean"]:
            shutil.rmtree(config["output_path"])
            os.mkdir(config["output_path"])
        scan_dirs()
