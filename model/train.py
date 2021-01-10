import numpy as np
from tensorflow.keras import layers, models, callbacks, optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
import os
from matplotlib import pyplot as plt
import glob

# Consts
image_shape = [244,244]
epochs = 6
NUMBER_OF_LABELS = 2
LEARNING_RATE = 1e-4
VALIDATION_SPLIT = 0.2
BATCH_SIZE = 8

def convert_to_one_hot(Y, C):
    Y = np.eye(C)[Y.reshape(-1)].T
    return Y

# Imports photos from good and bad folders
folders = glob.glob('photos/*')
imagenames_list = []
labels = []

l = 0
for folder in folders:
    for f in glob.glob(folder+'/*.jpg'):
        imagenames_list.append(f)
        labels.append(l)
    l += 1

read_images = []        
for image in imagenames_list:
    image_grey = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    image_borders = cv2.Canny(image_grey, 100, 200)
    read_images.append(cv2.resize(image_borders, (image_shape[0], image_shape[1]), interpolation = cv2.INTER_AREA))

# Convert to numpy and normalize
images = np.asarray(read_images)
labels = np.asarray(labels).astype(int)

indices = np.arange(labels.shape[0])
np.random.shuffle(indices)
images = images[indices]
labels = labels[indices]

n = len(read_images)
X = (images/255.).reshape(n, image_shape[0], image_shape[1], 1)
# Convert labels to one-hot encoding
Y = convert_to_one_hot(labels, NUMBER_OF_LABELS).T

val_index = int(n*(1-VALIDATION_SPLIT))
print(val_index)
X_train = X[0:val_index]
X_test = X[val_index:-1]
Y_train = Y[0:val_index]
Y_test = Y[val_index:-1]

datagen = ImageDataGenerator(
    # width_shift_range = 2,
    # height_shift_range = 2,
    shear_range = 0.15,
    # zoom_range = 0.1,
    # fill_mode = "nearest"
)   
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu',
                             input_shape=(image_shape[0], image_shape[1], 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(NUMBER_OF_LABELS, activation='softmax'))

model.compile(loss='binary_crossentropy',
                   optimizer=optimizers.RMSprop(lr=LEARNING_RATE),
                   metrics=['acc'])

history_conv = model.fit(datagen.flow(X_train, Y_train, batch_size=BATCH_SIZE), validation_data=(X_test, Y_test), epochs=epochs)

model_name = "posture_model_canny_aug.h5"
model.save(model_name)