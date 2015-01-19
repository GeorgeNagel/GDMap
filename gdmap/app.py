from flask import Flask, render_template

from gdmap.settings import FLASK_DEBUG
from gdmap.query import get_query_results

app = Flask(__name__)


@app.route('/')
def index():
    content = get_query_results()
    return render_template('base.html', content=content)


@app.route('/<terms>')
def terms_search(terms):
    content = get_query_results(terms=terms)
    return render_template('base.html', content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=FLASK_DEBUG)
