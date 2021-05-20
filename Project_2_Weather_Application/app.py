from flask.helpers import flash, url_for
from utils.weather import Weather
from flask import Flask , request , render_template , redirect
import requests
import json

# Temp Accoubt
email = "lifires218@firmjam.com"
password = "takemehome"

app = Flask(__name__)
weather = Weather()

app.config['SECRET_KEY'] = 'dattebayo!'


@app.route('/' , methods=['GET' , 'POST'])
def index():
    if(request.method == 'POST'):
        city_name = request.form['city']
        
        return redirect(url_for('weather_city' , city = city_name))
    
    return render_template('__home_page.html')

@app.route('/weather/<city>')
def weather_city(city):
    info = weather.get_info(city)
    
    if(info == None):
        flash('Invalid Country Name!!')
        return redirect(url_for('index'))
    
    return render_template('__search_results.html' , info = info)
