from flask import render_template

from gdmap import app


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/songs/')
def songs():
    return render_template('base.html')


@app.route('/search/', defaults={'query': None})
@app.route('/search/<query>')
def search(query):
    return render_template('base.html')
