import cv2
import numpy as np
from keras import models

classes = ["Bad", "Good"]

image = cv2.resize(cv2.imread('photos/good/test_10.jpg', cv2.IMREAD_GRAYSCALE), (244, 244), interpolation = cv2.INTER_AREA)
image = (image/255.).reshape(1, image.shape[0], image.shape[1], 1)

mymodel = models.load_model('posture_model.h5')
predictions = mymodel.predict(image)
class_pred = np.argmax(predictions)
conf = predictions[0][class_pred]
print(predictions)