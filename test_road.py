import unet

import os
import numpy as np
import cv2

from skimage import img_as_ubyte
from skimage.util import view_as_windows, pad
from sklearn.metrics import classification_report

# Obtained Results
#               precision    recall  f1-score   support

#          0.0       0.98      0.99      0.99 105069645
#          1.0       0.81      0.67      0.73   5180355

#     accuracy                           0.98 110250000
#    macro avg       0.90      0.83      0.86 110250000
# weighted avg       0.98      0.98      0.98 110250000


def get_prediction_masks(patch_predictions):
    patch_size = (256, 256)
    patches_per_row = 6
    patches_per_col = 6
    patches_per_image = 36
    num_images = patch_predictions.shape[0] // patches_per_image
    original_image_size = (1500, 1500)
    prediction_size = (1536, 1536)
    prediction_masks = np.zeros((num_images, ) + original_image_size)

    for k in range(num_images):
        mask_prediction = patch_predictions[k * patches_per_image:
                                            (k + 1) * patches_per_image]
        mask_prediction = mask_prediction.reshape(
            (patches_per_image, ) + patch_size
        )
        prediction = np.zeros(prediction_size)
        for i in range(patches_per_image):
            prediction[int(i / patches_per_col) * patch_size[1]:(
                int(i / patches_per_col) + 1
            ) * patch_size[1], (i % patches_per_row) * patch_size[0]:(
                (i % patches_per_row) + 1
            ) * patch_size[0]] = mask_prediction[i]
        prediction = prediction[:original_image_size[0], :original_image_size[1]]
        cv2.imwrite('road_predictions/%d_before_threshold.jpg'%(k+1), img_as_ubyte(prediction))
        prediction[prediction > 0.5] = 1.
        prediction[prediction <= 0.5] = 0.
        cv2.imwrite('road_predictions/%d.jpg'%(k+1), img_as_ubyte(prediction))
        prediction_masks[k] = prediction

    return prediction_masks


def test_generator(test_dir, image_dir, num_image=49):
    
    patch_size=(256, 256, 1)
    pad_width = ((0, 36), (0, 36), (0, 0))
    image_pad_values = ((1., 1.), (1., 1.), (1., 1.))
    original_image_size=(1500, 1500)

    for i in range(1, num_image + 1):
        
        image = cv2.imread(
            os.path.join(test_dir, image_dir, '%d.jpg' % i), 0
        )
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

# generating building map for testing images
test_data_dir = '../road_data/test/'
save_model_path = 'saved_model/unet_road_detection.hdf5'
original_image_size = (1500, 1500)
test_num_images = 49

test_data = test_generator(
    test_data_dir,
    'images',
    num_image=test_num_images
)

model = unet.unet(input_size=(256, 256, 1))
model.load_weights(save_model_path)

patch_predictions = model.predict_generator(
    test_data, steps=test_num_images, verbose=1
)
prediction_masks = get_prediction_masks(
    patch_predictions=patch_predictions
)

# loading original labels/masks for score calculation
original_masks = np.zeros((test_num_images, 1500, 1500))
for i in range(1, test_num_images + 1):
    mask = cv2.imread(os.path.join(test_data_dir, 'labels', '%d.jpg' % i), 0)
    mask = cv2.resize(mask, original_image_size)
    mask = mask / 255.
    mask[mask > 0.5] = 1.
    mask[mask <= 0.5] = 0.
    original_masks[i - 1] = mask

# calculating scores
prediction_masks = prediction_masks.reshape(-1)
original_masks = original_masks.reshape(-1)
print(classification_report(original_masks, prediction_masks))
