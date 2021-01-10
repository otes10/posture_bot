import cv2
import numpy as np
from keras import models
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


classes = ["Bad", "Good"]

def load_images_from_folder(folder):
    images = []
    filenames = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
            filenames.append(filename)
    return (filenames,images)

mymodel = models.load_model('posture_model_canny_aug.h5')

# Predicts all images from model/testing
filenames, images = load_images_from_folder('demo')

for image in images:
    for i in range(len(images)):
        a = image == images[i]
        if a.all():
            index = i
    filename = filenames[index]

    image = cv2.Canny(image, 100, 200)
    image = cv2.resize(image, (244, 244), interpolation = cv2.INTER_AREA)
    image = (image/255.).reshape(1, image.shape[0], image.shape[1], 1)
    predictions = mymodel.predict(image)

    bad, good = predictions[0].tolist()
    class_pred = np.argmax(predictions)
    conf = predictions[0][class_pred]

    print('\033[1m'+'\033[94m'+f"Analyzing file {filename}...")

    if classes[class_pred] == 'Bad':
        print('\033[91m'+f"{filename} shows someone with BAD posture")
        print(f"Confidence in data: {round(conf*100,4)}%"+'\033[0m')
    elif classes[class_pred] == 'Good':
        print('\033[92m'+f"{filename} shows someone with GOOD posture")
        print(f"Confidence in data: {round(conf*100,4)}%"+'\033[0m')