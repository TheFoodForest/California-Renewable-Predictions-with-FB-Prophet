"""
Flask views for rendering templates 

"""
## Flask file creating the routes for the rendering and getting data from db

from flask import render_template
from Renewable_App import app

## Siple routes for now just rendering templates, might pass some data in for jinja templating 
## Might make some page that renders redirects

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predictions')
def predictions():
    return render_template('predictions.html')

@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/solar')
def solar():
    return render_template('solar.html')

@app.route('/wind')
def wind():
    return render_template('wind.html')

@app.route('/other')
def other():
    return render_template('other.html')
