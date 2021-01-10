import requests
import glob

# this filters the images using regex based on a directory you want to send it from, so change the reference location accordingly
good_photos = glob.glob("/home/pi/nwhacks/photos/good/*.jpg")
bad_photos = glob.glob("/home/pi/nwhacks/photos/bad/*.jpg")

url = 'http://127.0.0.1:5000/current'

date = {'date': '2021_1_9'}

# request daily report
r = requests.post(url, params=date)
print(r.json())

data = {'date': '2021_1_9', 'hour':'21'}
# request hourly report
url = 'http://127.0.0.1:5000/hourly'
r = requests.post(url, params=data)
print(r.json())