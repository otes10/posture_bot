from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from keras import models
import numpy as np
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array
# display the image on screen and wait for a keypress
cv2.imwrite("test_1.jpg", image)
image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
image = cv2.Canny(image, 100, 200)
image = cv2.resize(image, (244,244))

image = (image/255.).reshape(1, image.shape[0], image.shape[1], 1)
mymodel = models.load_model('posture_model_canny.h5')
predictions = mymodel.predict(image)
class_pred = np.argmax(predictions)
conf = predictions[0][class_pred]
print(predictions)