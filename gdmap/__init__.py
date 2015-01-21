from flask import Flask

app = Flask(__name__)

# Delayed import to avoid cirular references
import gdmap.views  # noqa
