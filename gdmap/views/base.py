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


@app.route('/recording/<show_id>')
def recording(show_id):
    return render_template('base.html')


@app.route('/recordings/', defaults={'query': None})
@app.route('/recordings/<query>')
def recordings(query):
    return render_template('base.html')
