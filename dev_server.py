"""Run the flask development server."""
from gdmap import app
from gdmap.settings import FLASK_DEBUG

app.run(host="0.0.0.0", port=80, debug=FLASK_DEBUG)
