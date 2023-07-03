from flask import Flask, request
from flask_restful import Resource, Api
from .tasks import eigen
import time
import os, random

app = Flask(__name__)
api = Api(app)

class Eigen(Resource):
    def __init__(self):
        return
    def get(self, seed):
        submitted = eigen.delay(seed)
        # while not submitted.ready():
        #     time.sleep(0.5)
        return submitted.get()

api.add_resource(Eigen, '/<int:seed>')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
