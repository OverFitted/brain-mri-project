#!/usr/bin/env python
# coding: utf-8

from pydicom import dcmread
from glob import glob

import cv2
import numpy as np
import os
import pydicom
import re
import shutil
import zipfile

from config import *


def dcm2imgseq(path):
    """Convert dicom archive to image sequence

    Args:
        path (str): dicom archive path
    """
    # creating folders
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    for folder in glob(os.path.join(IMAGE_FOLDER, "*", "")):
        shutil.rmtree(folder)

    # reading zipfile
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(DATA_FOLDER)

    # converting .dcm to .jpg
    sequences = [os.path.split(seq)[-1] for seq in glob(os.path.join(DATA_FOLDER, "*"))]
    for seq in sequences:
        os.makedirs(os.path.join(IMAGE_FOLDER, seq))
        for i, dcm_path in enumerate(sorted(os.listdir(os.path.join(DATA_FOLDER, seq)), key=lambda x: int("".join([s for s in list(x) if s.isdigit()])))):
            dc = dcmread(os.path.join(DATA_FOLDER, seq, dcm_path), force=True)
            image = dc.pixel_array

            normalized_image = np.zeros(image.shape)
            normalized_image = cv2.normalize(image, normalized_image, 0, 256, cv2.NORM_MINMAX)

            cv2.imwrite(os.path.join(IMAGE_FOLDER, seq, f"{i}.jpg"), normalized_image)

    # removing folder
    shutil.rmtree(DATA_FOLDER)

    return sequences


if __name__ == "__main__":
    dcm2imgseq('test.zip')
