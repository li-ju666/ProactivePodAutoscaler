from random import randint, choice, uniform
import requests
from time import sleep
import time

# Job definitions
raw_urls = ["http://entrypoint0:5000/sort/","http://entrypoint0:5000/eigen/"]

with open('/nasa_request.txt', 'r') as f:
    req_data = f.read().split('\n')[:-1]

req_data = [2*int(s) for s in req_data]

def access_url(url):
    response = requests.get(url, timeout=20)
    try:
        result = response.json()
    except:
        result = response.content
    print(url, result, flush=True)

minute = 0
for num in req_data:
    minute += 1
    with open('/progress.log', 'a+') as f:
        f.write("Min :{}\n  Rate: {}\n".format(minute, num))
    sleep_time = 60/num - 0.5156
    if sleep_time < 0: 
        sleep_time = 0
    for i in range(num):
        sleep(sleep_time)
        job = raw_urls[choice([0]*19+[1])]+str(randint(0, 1000))
        try:
            start = time.time()
            access_url(job)
            restime = time.time() - start
            if 'sort' in job:
                with open('/sort_response.log', 'a+') as f:
                    f.write(str(restime) + '\n')
            else: 
                with open('/eigen_response.log', 'a+') as f:
                    f.write(str(restime) + '\n')
        except: 
            continue

