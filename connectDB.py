import pymongo
from pymongo import MongoClient


def connectDB():
    client = MongoClient('218.150.247.209:2017',
                         username='unsik',
                         password='',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256')
    return client
