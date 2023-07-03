from project.celery import app
import numpy, os, time, requests

@app.task
def sort(seed):
    start = time.time()
    dim = 2500
    n = dim*dim
    numpy.random.seed(seed)
    a = numpy.random.rand(1, n)
    a.sort()
    return str(time.time()-start)

@app.task
def eigen(seed):
    response = requests.get('http://{}:5000/'.format(os.getenv('EIG_SERVER'))+str(seed))
    return response.json()
