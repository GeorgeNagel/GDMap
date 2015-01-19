from flask import Flask, render_template

from gdmap.es_index import es
from gdmap.settings import FLASK_DEBUG

app = Flask(__name__)


@app.route('/')
def index():
    content = es.search(index="gdmap", body={"query": {"match_all": {}}})
    return render_template('base.html', content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=FLASK_DEBUG)
