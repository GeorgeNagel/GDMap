from flask import render_template

from gdmap import app
from gdmap.query import get_query_results


@app.route('/')
def index():
    content = get_query_results()
    return render_template('base.html', content=content)


@app.route('/songs/')
def songs():
    content = get_query_results()
    return render_template('base.html', content=content)
