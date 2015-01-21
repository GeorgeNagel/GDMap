from flask import Flask
from flask.ext.restful import Api

app = Flask(__name__)
api = Api(app)

# Delayed import to avoid cirular references
import gdmap.views  # noqa
