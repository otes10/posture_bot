from aws import get_object, get_total_bytes

import json

filename = '/photos/2021_1_10_3_27.jpg'

total_bytes = get_total_bytes(filename)
data = get_object(total_bytes, filename)

print(type(data))

f = open('./test_download.png','wb')
f.write(data)
f.close()
