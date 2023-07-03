from project.celery import app
import numpy, time

@app.task
def eigen(seed):
    start = time.time()
    dim = 1000
    n = dim * dim
    numpy.random.seed(seed)
    a = numpy.random.rand(dim, dim)
    b = numpy.linalg.eig(a)
    # response = requests.get('http://eigenserver:5000/'+str(seed))
    return str(time.time()-start)
