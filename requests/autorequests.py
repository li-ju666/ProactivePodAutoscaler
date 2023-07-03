from random import randint, choice, uniform
import requests
from time import sleep

# Job definitions
raw_urls = ["http://localhost:5000/sort/", "http://localhost:5000/eigen/"]

def access_url(url):
    response = requests.get(url)
    try:
        result = response.json()
    except:
        result = response.content
    print(url, result, flush=True)

index = 0
while True: 
    batch_size = randint(200, 400)
    minT, maxT = choice([(0.1, 0.2) , (0.5, 1), (2, 4)])
    for i in range(batch_size):
        print(index)
        index += 1
        # sleep(uniform(minT, maxT))
        stime = uniform(minT, maxT)
        print("sleep time: {}".format(stime))
        sleep(stime)
        job = raw_urls[choice([0]*19+[1])]+str(randint(0, 1000))
        access_url(job)

