'''
CTP缺血区域计算连通域
2020-01-15
'''


#!/usr/bin/env python
# coding: utf-8

from skimage import measure
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os

np.set_printoptions(threshold=1e-8)

class Read_file():
    def __init__(self, path):
        self.path = path
        self.img = None
        self.message = dict()
    def read_single_dicom(self):
        file = sitk.ReadImage(self.path)
        self.img = sitk.GetArrayFromImage(file)
        self.img = np.squeeze(self.img)
        return self.img
    def read_series_dicom(self):
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(self.path)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()
        self.img = sitk.GetArrayFromImage(image) # z, y, x
        self.message['origin'] = image.GetOrigin() # x, y
        self.message['spacing'] = image.GetSpacing() # x, y, z
        return self.img
    def get_message(self):
        return self.message


def cpt(path, series=True):
    # read dicom
    if series:
        image_array = Read_file(path).read_series_dicom()
    else:
        image_array = Read_file(path).read_single_dicom()

    # convert to 0 or 1
    connv = image_array>0

    connv = measure.label(connv, connectivity=1)   #   Label connected regions of an integer array.
    connv_flatten = connv.flatten()
    connv_counter = dict(Counter(connv_flatten))  # dict subclass for counting hashable objects
    connv_counter = sorted(connv_counter.items(), key= lambda d:d[1],
                           reverse=True)
    real_image = image_array * (connv==connv_counter[1][0])
    if series:
        for i in range(image_array.shape[0]):
            plt.figure()
            plt.imshow(image_array[i], cmap='gray')
            plt.figure()
            plt.imshow(real_image[i], cmap='gray')
    else:
        plt.figure()
        plt.imshow(image_array, cmap='gray')
        plt.figure()
        plt.imshow(real_image, cmap='gray')


case_path  = '/home/lfy/data/chenyupei/case3_Tmax'
file_list = os.listdir(case_path)
file_list.sort()
for file in file_list:
    print(file)
    cpt(os.path.join(case_path, file), series=False)

case_path  = '/home/lfy/data/chenyupei/case3_Tmax'
cpt(case_path, series=True)

