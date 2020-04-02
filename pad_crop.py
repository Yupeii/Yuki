'''
pad crop and reslice images
2020-04-02

'''


import numpy as np

def pad(img, shape):
    """pad an image to transorm it into a specified shape, does not cut the image
    if output size is smaller"""
    delta_h = shape[0]-img.shape[0]
    delta_w = shape[1]-img.shape[1]
    if delta_h > 0:
        up = delta_h//2
        down = delta_h-up
        img = np.vstack((np.zeros((up,img.shape[1]), dtype=np.float32), img))
        img = np.vstack((img, np.zeros((down,img.shape[1]), dtype=np.float32)))
    if delta_w > 0:
        left = delta_w//2
        right = delta_w-left
        img = np.hstack((np.zeros((img.shape[0],left), dtype=np.float32), img))
        img = np.hstack((img, np.zeros((img.shape[0], right), dtype=np.float32)))
    return img

def crop(img, shape):
    """pad an image to transorm it into a specified shape, does not cut the image
    if output size is smaller"""
    delta_h = img.shape[0]-shape[0]
    delta_w = img.shape[1]-shape[1]
    if delta_h > 0:
        up = delta_h//2
        down = delta_h-up
        img = img[up:-down,:]
    if delta_w > 0:
        left = delta_w//2
        right = delta_w-left
        img = img[:,left:-right]
    return img

def pad_crop(img, shape):
    """aplly padding and cropping to resize the current image without rescaling"""
    img = pad(img, shape)
    img = crop(img, shape)
    return img

def resize_slices_cxy(slices, shape):
    resized = np.empty((slices.shape[0], shape[0], shape[1]), dtype=np.float32)
    for i in range(slices.shape[0]):
        resized[i] = pad_crop(slices[i], shape)
    return resized

def resize_slices_xyc(slices, shape):
    resized = np.empty((shape[0], shape[1], slices.shape[2]), dtype=np.float32)
    for i in range(slices.shape[2]):
        resized[:,:,i] = pad_crop(slices[:,:,i], shape)
    return resized

