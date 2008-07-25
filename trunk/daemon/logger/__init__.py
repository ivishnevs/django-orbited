from log import setup
from config import map as configmap

logroot = setup(configmap)


def get_logger(name):
    return logroot.get_logger(name)
