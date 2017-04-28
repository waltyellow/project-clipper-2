from flask import Flask

server = Flask(__name__)

from app import main

import logging
logging.basicConfig(filename='global.log', level=logging.DEBUG)
