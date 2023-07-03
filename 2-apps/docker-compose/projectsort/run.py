from flask import Flask, request
from flask_restful import Resource, Api

from .tasks import sort, eigen
import time
import os, random

app = Flask(__name__)
api = Api(app)

class SortAndMedian(Resource):
    def __init__(self):
        return

    def get(self, seed):
        submitted = sort.delay(seed)
        return submitted.get()

class Eigen(Resource):
    def __init__(self):
        return

    def get(self, seed):
        submitted = eigen.delay(seed)
        return submitted.get()

api.add_resource(SortAndMedian, '/sort/<int:seed>')
api.add_resource(Eigen, '/eigen/<int:seed>')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
