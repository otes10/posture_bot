import time
import datetime
from dateutil.tz import gettz

from picamera import PiCamera
from random import randint
import json

from aws import upload_file
from io import BytesIO

import cv2
import numpy as np
from keras import models

# Config options
FILE_LOCATION_PHOTOS = '/photos/'
FILE_LOCATION_API = '/home/pi/nwhacks/api/data/'
TIMEZONE = 'America/Los Angeles'
classes = ["Bad", "Good"]

# Helper methods
def image_analysis(image_stream):
    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.Canny(img, 100, 200)
    img = cv2.resize(img, (244,244))

    img = (img/255.).reshape(1, img.shape[0], img.shape[1], 1)
    mymodel = models.load_model('/home/pi/nwhacks/api/model_dev.h5')

    predictions = mymodel.predict(img)
    
    # returns a tuple of % good and % bad
    return tuple(predictions[0].tolist())

time_now = datetime.datetime.now(gettz(TIMEZONE))
date = time_now.date()
hour_min = time_now.time()

# Save a current date + time for filename
##Change column to underscore because crashes on pc
timestr = str(date.year) + '_' + str(date.month) + '_' + str(date.day) + "_" + str(hour_min.hour) + '_' + str(hour_min.minute)
img_file = FILE_LOCATION_PHOTOS + timestr + '.jpg'

datastr = str(date.year) + '_' + str(date.month) + '_' + str(date.day)
data_file = FILE_LOCATION_API + datastr + '.json'

# Camera Setup
camera = PiCamera(resolution=(1280, 720), framerate=30)

## Set ISO
camera.iso = 1400

## Automatic gain control delay
time.sleep(2)

## Fixed values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

# Finally, take a photo with the fixed settings
img_ = BytesIO()
camera.capture(img_, 'jpeg')
img_.seek(0)
upload_file(img_, img_file)

bad, good = image_analysis(img_)
bad = float(bad*100)
good = float(good*100)
print(bad)
print(good)

data = {}
data['img_file'] = img_file
data['hour'] = str(hour_min.hour)
data['minute'] = str(hour_min.minute)
data['posture'] = {'good':good, 'bad':bad}


import os
# check if size of file is 0

if not os.path.exists(data_file):
    prev = []
    open(data_file,'a').close() 
# if file is empty
elif os.path.getsize(data_file) == 0:
    prev = []
else:
    prev = json.load(open(data_file, 'r'))
    print(prev)



# Append new dictionary entry to end of the list
prev.append(data)

# Change this to store a list of JSON rather than append JSON dictionaries to the end of the file
json.dump(prev,open(data_file, "w"), indent=3)