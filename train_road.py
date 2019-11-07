import unet

import numpy as np
from skimage.util import view_as_windows, pad

from keras.callbacks import ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator

def get_patches(image, mask):
    
    patch_size = (256, 256, 1)
    pad_width = ((0, 36), (0, 36), (0, 0))
    image_pad_values = ((1., 1.), (1., 1.), (1., 1.))
    mask_pad_values = ((0., 0.), (0., 0.), (0., 0.))
    patches_per_image = 36
    
    image_patches_batch = np.zeros(
        (patches_per_image, ) + patch_size
    )
    mask_patches_batch = np.zeros(
        (patches_per_image, ) + patch_size
    )

    image = pad(
        image,
        pad_width=pad_width,
        mode='constant',
        constant_values=image_pad_values
    )
    mask = pad(
        mask,
        pad_width=pad_width,
        mode='constant',
        constant_values=mask_pad_values
    )

    image_patches = view_as_windows(
        image, window_shape=patch_size, step=patch_size
    ).reshape((-1, ) + patch_size)
    mask_patches = view_as_windows(
        mask, window_shape=patch_size, step=patch_size
    ).reshape((-1, ) + patch_size)

    return zip(image_patches, mask_patches)

def data_generator(data_dir, images_dir, masks_dir):

    # we create two instances with the same arguments
    data_gen_args = dict(rotation_range=45,
                     width_shift_range=0.1,
                     height_shift_range=0.1,
                     rescale=1/255.,
                     zoom_range=0.2)

    image_datagen = ImageDataGenerator(**data_gen_args)
    mask_datagen = ImageDataGenerator(**data_gen_args)

    seed = 1

    image_generator = image_datagen.flow_from_directory(
        data_dir,
        classes = [images_dir],
        class_mode=None,
        batch_size=1,
        seed=seed)
    mask_generator = mask_datagen.flow_from_directory(
        data_dir,
        classes = [masks_dir],
        class_mode=None,
        batch_size=1,
        seed=seed)

    # generating image patches and then training model to preven data loss
    for image_batch, mask_batch in zip(image_generator, mask_generator):
        mask_batch[mask_batch > 0.5] = 1.
        mask_batch[mask_batch <= 0.5] = 0.
        for image, mask in zip(image_batch, mask_batch):
            for image_patch, mask_patch in get_patches(image, mask):
                yield (np.expand_dims(image_patch, axis=0), 
                	np.expand_dims(mask_patch, axis=0)
                )

train_data_dir = '../road_data/train/'
val_data_dir = '../road_data/val/'
train_data = data_generator(train_data_dir, 'images', 'labels')
validation_data = data_generator(val_data_dir, 'images', 'labels')

save_model_path = 'saved_model/unet_road_detection.hdf5'
model = unet.unet(input_size=(256, 256, 1))
model_checkpoint = ModelCheckpoint(
    save_model_path,
    monitor='val_loss',
    save_best_only=True
)
model.fit_generator(
    train_data,
    steps_per_epoch=10000,
    validation_data=validation_data,
    validation_steps=1000,
    epochs=10,
    callbacks=[model_checkpoint]
)