import unet

import os
import sys
import numpy as np
import cv2

from skimage import img_as_ubyte
from skimage.util import view_as_windows, pad
from sklearn.metrics import classification_report

def get_dii(pre_mask, post_mask):
    diff_pixels = post_mask - pre_mask
    diff_pixels[diff_pixels >= 0] = 0.0
    diff_pixels[diff_pixels < 0] = 1.0
    return (diff_pixels.sum() / pre_mask.sum()) * 36

def get_prediction_mask(mask_prediction):
    patch_size = (256, 256)
    prediction_size = (1536, 1536)
    original_image_size = (1500, 1500)
    patches_per_row = 6
    patches_per_col = 6
    patches_per_image = 36

    prediction = np.zeros(prediction_size)
    for i in range(patches_per_image):
        prediction[int(i / patches_per_col) * patch_size[1]:(
            int(i / patches_per_col) + 1
        ) * patch_size[1], (i % patches_per_row) * patch_size[0]:(
            (i % patches_per_row) + 1
        ) * patch_size[0]] = mask_prediction[i]
    prediction = prediction[:original_image_size[0], :original_image_size[1]]

    return prediction

def image_to_patches(image):
    patch_size=(256, 256, 1)
    pad_width = ((0, 36), (0, 36), (0, 0))
    image_pad_values = ((1., 1.), (1., 1.), (1., 1.))
    original_image_size=(1500, 1500)

    image = cv2.resize(image, original_image_size)
    image = image.reshape(original_image_size + (1, ))

    image = pad(
        image,
        pad_width=pad_width,
        mode='constant',
        constant_values=image_pad_values
    )
    image_patches = view_as_windows(
        image, window_shape=patch_size, step=patch_size
    ).reshape((-1, ) + patch_size)
    image_patches = image_patches / 255.

    yield image_patches

def get_predictions(pre_image_filename, post_image_filename):
    pre_image = cv2.imread(pre_image_filename, 0)
    post_image = cv2.imread(post_image_filename, 0)

    building_model_path = 'saved_model/unet_building_detection.hdf5'
    building_model = unet.unet(input_size=(256, 256, 1))
    building_model.load_weights(building_model_path)
    pre_image_generator = image_to_patches(pre_image)
    post_image_generator = image_to_patches(post_image)
    pre_image_buildings = building_model.predict_generator(pre_image_generator, steps=1, verbose=1)
    post_image_buildings = building_model.predict_generator(post_image_generator, steps=1, verbose=1)
    pre_image_buildings = get_prediction_mask(pre_image_buildings.reshape(36, 256, 256))
    post_image_buildings = get_prediction_mask(post_image_buildings.reshape(36, 256, 256))
    pre_image_buildings[pre_image_buildings > 0.5] = 1.0
    pre_image_buildings[pre_image_buildings <= 0.5] = 0.0
    post_image_buildings[post_image_buildings > 0.5] = 1.0
    post_image_buildings[post_image_buildings <= 0.5] = 0.0

    road_model_path = 'saved_model/unet_road_detection.hdf5'
    road_model = unet.unet(input_size=(256, 256, 1))
    road_model.load_weights(road_model_path)
    pre_image_generator = image_to_patches(pre_image)
    post_image_generator = image_to_patches(post_image)
    pre_image_roads = road_model.predict_generator(pre_image_generator, steps=1, verbose=1)
    post_image_roads = road_model.predict_generator(post_image_generator, steps=1, verbose=1)
    pre_image_roads = get_prediction_mask(pre_image_roads.reshape(36, 256, 256))
    post_image_roads = get_prediction_mask(post_image_roads.reshape(36, 256, 256))
    pre_image_roads[pre_image_roads > 0.5] = 1.0
    pre_image_roads[pre_image_roads <= 0.5] = 0.0
    post_image_roads[post_image_roads > 0.5] = 1.0
    post_image_roads[post_image_roads <= 0.5] = 0.0

    pre_mask = pre_image_buildings + pre_image_roads
    post_mask = post_image_buildings + post_image_roads
    pre_mask[pre_mask > 0.5] = 1.0
    pre_mask[pre_mask <= 0.5] = 0.0
    post_mask[post_mask > 0.5] = 1.0
    post_mask[post_mask <= 0.5] = 0.0

    dii = get_dii(pre_mask, post_mask)

    post_image = cv2.imread(post_image_filename)
    green_mask = np.zeros((post_image.shape))
    red_mask = np.zeros((post_image.shape))
    distroyed_pixels = []
    added_pixels = []

    for i in range(1500):
        for j in range(1500):
            if pre_mask[i][j] == 1.0 and post_mask[i][j] == 0.0:
                red_mask[i][j][2] += 255
                distroyed_pixels.append((i,j))
            elif pre_mask[i][j] == 0.0 and post_mask[i][j] == 1.0:
                green_mask[i][j][1] += 255
                added_pixels.append((i,j))
    post_image = green_mask*0.75 + post_image;
    post_image = red_mask*0.75 + post_image;
    
    # pre_mask = img_as_ubyte(pre_mask)
    # post_mask = img_as_ubyte(post_mask)
    # cv2.imwrite('pre.jpg', pre_mask)
    # cv2.imwrite('post.jpg', post_mask)
    
    return post_image, dii, added_pixels, distroyed_pixels

# get_predictions(sys.argv[1], sys.argv[2])