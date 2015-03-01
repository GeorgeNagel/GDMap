from flask import render_template

from gdmap import app


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/songs/', defaults={'query': None})
@app.route('/songs/<query>')
def songs(query):
    return render_template('base.html')


@app.route('/search/', defaults={'query': None})
@app.route('/search/<query>')
def search(query):
    return render_template('base.html')


@app.route('/show/<show_id>')
def show(show_id):
    return render_template('base.html')
