# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 0026 下午 1:57
# @Author  : oyj
# @Email   : 1272662747@qq.com
# @File    : CNNComponents.py
# @Software: PyCharm
import sys

import numpy

def conv_processor(img, conv_filter):
    filter_size = conv_filter.shape[1]
    result_matrix = numpy.zeros(img.shape)
    for r in numpy.uint16(numpy.arange(filter_size/2.0,
                          img.shape[0]-filter_size/2.0+1)):
        for c in numpy.uint16(numpy.arange(filter_size/2.0,
                                           img.shape[1]-filter_size/2.0+1)):
            curr_region = img[r-numpy.uint16(numpy.floor(filter_size/2.0)):r+numpy.uint16(numpy.ceil(filter_size/2.0)),
                          c-numpy.uint16(numpy.floor(filter_size/2.0)):c+numpy.uint16(numpy.ceil(filter_size/2.0))]
            curr_resultMatrix = curr_region * conv_filter
            curr_result = numpy.sum(curr_resultMatrix)
            result_matrix[r, c] = curr_result
    final_result = result_matrix[numpy.uint16(filter_size/2.0):result_matrix.shape[0]-numpy.uint16(filter_size/2.0),
                          numpy.uint16(filter_size/2.0):result_matrix.shape[1]-numpy.uint16(filter_size/2.0)]
    return final_result




def conv(img, conv_filter):
    if len(img.shape) > 2 or len(conv_filter.shape) > 3:  # Check if number of image channels matches the filter depth.
        if img.shape[-1] != conv_filter.shape[-1]:
            print("Error: Number of channels in both image and filter must match.")
            sys.exit()
    if conv_filter.shape[1] != conv_filter.shape[2]:  # Check if filter dimensions are equal.
        print('Error: Filter must be a square matrix. I.e. number of rows and columns must match.')
        sys.exit()
    if conv_filter.shape[1] % 2 == 0:  # Check if filter diemnsions are odd.
        print('Error: Filter must have an odd size. I.e. number of rows and columns must be odd.')
        sys.exit()

        # An empty feature map to hold the output of convolving the filter(s) with the image.
    feature_maps = numpy.zeros((img.shape[0] - conv_filter.shape[1] + 1,
                                img.shape[1] - conv_filter.shape[1] + 1,
                                conv_filter.shape[0]))

    # Convolving the image by the filter(s).
    for filter_num in range(conv_filter.shape[0]):
        print("Filter ", filter_num + 1)
        curr_filter = conv_filter[filter_num, :]  # getting a filter from the bank.
        """ 
        Checking if there are mutliple channels for the single filter.
        If so, then each channel will convolve the image.
        The result of all convolutions are summed to return a single feature map.
        """
        print(curr_filter.shape)
        if len(curr_filter.shape) > 2:
            conv_map = conv_processor(img[:, :, 0], curr_filter[:, :, 0])  # Array holding the sum of all feature maps.
            for ch_num in range(1, curr_filter.shape[
                -1]):  # Convolving each channel with the image and summing the results.
                conv_map = conv_map + conv_processor(img[:, :, ch_num],
                                            curr_filter[:, :, ch_num])
        else:  # There is just a single channel in the filter.
            conv_map = conv_processor(img, curr_filter)
        feature_maps[:, :, filter_num] = conv_map  # Holding feature map with the current filter.
    return feature_maps  # Returning all feature maps.

def pooling(feature_maps, stride = 2, size = 2):
    pool_matrix = numpy.zeros((numpy.uint16((feature_maps.shape[0]-size+1) / stride + 1),
                              numpy.uint16((feature_maps.shape[1] - size + 1) / stride + 1),
                              feature_maps.shape[-1]))
    for num in range(feature_maps.shape[-1]):
        r2 = 0
        for r in numpy.arange(0, feature_maps.shape[0] - size + 1, stride):
            c2 = 0
            for c in numpy.arange(0, feature_maps.shape[1] - size + 1, stride):
                pool_matrix[r2, c2, num] = numpy.max([feature_maps[r:r+size,  c:c+size]])
                c2 = c2 + 1
            r2 = r2 + 1
    return pool_matrix


def relu(feature_maps):
    rele_out = numpy.zeros(feature_maps.shape)
    for num in range(feature_maps.shape[-1]):
        for r in numpy.arange(0, feature_maps.shape[0]):
            for c in numpy.arange(0, feature_maps.shape[1]):
                rele_out[r, c, num] = numpy.max([0, feature_maps[r, c, num]])
    return rele_out


