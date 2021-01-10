from time import sleep
from picamera import PiCamera

camera = PiCamera(resolution=(1280, 720), framerate=30)

# Set ISO
camera.iso = 1400

# Automatic gain control delay
sleep(2)

# Fixed values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

# Camera warm-up time
for i in range(30):
    camera.capture('photos/bad/test_{}.jpg'.format(i)) # referenced based on your working directory (/home/pi)
    sleep(1.5)