import cv2
import numpy as np
from keras import models
import os

classes = ["Bad", "Good"]

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
    return images

mymodel = models.load_model('posture_model_canny_aug.h5')

images = load_images_from_folder('testing')
i = 0
for image in images:
    image = cv2.Canny(image, 100, 200)
    image = cv2.resize(image, (244, 244), interpolation = cv2.INTER_AREA)
    image = (image/255.).reshape(1, image.shape[0], image.shape[1], 1)
    predictions = mymodel.predict(image)
    class_pred = np.argmax(predictions)
    conf = predictions[0][class_pred]
    print(classes[class_pred], conf)
    i += 1