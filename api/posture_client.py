import requests
import glob
# url = 'http://127.0.0.1:5000/current'

# date = {'date': '2021_1_10'}

# date = {'date': '2021_1_10'}
# request daily report
def get_daily_report(date):
    url = 'https://jolly-seahorse-2.loca.lt/current'
    r = requests.post(url, params=date)
    return r.json()

# # request hourly report
# data = {'date': '2021_1_10', 'hour':'9'}

def get_hourly_report(data):
    url = 'https://jolly-seahorse-2.loca.lt/hourly'
    r = requests.post(url, params=data)
    return r.json()

# Params: data = {'datetime': '2021_1_10_3_12'}
# Returns: a sequence of bytes

def get_timed_image(data):
    url = 'https://jolly-seahorse-2.loca.lt/image'
    r = requests.post(url, params=data)
    return r.content


date = {'date': '2021_1_10'}
print(get_daily_report(date))
data = {'date': '2021_1_10', 'hour':'9'}
print(get_hourly_report(data))
data = {'datetime': '2021_1_10_3_12'}
print(get_timed_image(data))