import requests
import glob

# this filters the images using regex based on a directory you want to send it from, so change the reference location accordingly
good_photos = glob.glob("/home/pi/nwhacks/photos/good/*.jpg")
bad_photos = glob.glob("/home/pi/nwhacks/photos/bad/*.jpg")

url = 'http://127.0.0.1:5000/current'

date = {'date': '2021_1_10'}

# request daily report
def get_daily_report(date):
    r = requests.post(url, params=date)
    return r.json()

# request hourly report
data = {'date': '2021_1_10', 'hour':'9'}

def get_hourly_report(data):
    url = 'http://127.0.0.1:5000/hourly'
    r = requests.post(url, params=data)
    return r.json()

# Params: data = {'datetime': '2021_1_10_3_12'}
# Returns: a sequence of bytes

def get_timed_image(data):
    url = 'http://127.0.0.1:5000/image'
    r = requests.post(url, params=data)
    return r.content

