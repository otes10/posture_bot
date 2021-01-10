import numpy as np
from tensorflow.keras import layers, models, callbacks
import cv2
import os
from matplotlib import pyplot as plt
import glob

# Consts
image_shape = [244,244]
epochs = 10
NUMBER_OF_LABELS = 2

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
    read_images.append(cv2.resize(cv2.imread(image, cv2.IMREAD_GRAYSCALE), (image_shape[0], image_shape[1]), interpolation = cv2.INTER_AREA))

# Convert to numpy and normalize
images = np.asarray(read_images)
n = len(read_images)
x = (images/255.).reshape(n, image_shape[0], image_shape[1], 1)
print(x.shape)
labels = np.asarray(labels).astype(int)

# Convert labels to one-hot encoding
Y = convert_to_one_hot(labels, NUMBER_OF_LABELS).T

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
                   optimizer='adam',
                   metrics=['acc'])

history_conv = model.fit(x, Y, epochs=epochs)

model_name = "posture_model.h5"
model.save(model_name)