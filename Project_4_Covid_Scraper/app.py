from flask import Flask , url_for , redirect , render_template , request
from utils.covid import Covid

#Creating A Flask And Covid Instance
app = Flask(__name__)
covid = Covid()

@app.route('/' , methods=["GET" , 'POST'])
def home_page():
    if(request.method == 'POST'):
        name = request.form['country']

        return redirect(url_for('country' , country_name = name))

    summary_cases = covid.get_summary_cases()
    
    countries_avail = covid.get_countries()

    return render_template('__home_page.html' , cases = summary_cases , country = countries_avail)

@app.route('/country/<country_name>')
def country(country_name):
    slug_name , country_name = country_name.split(';')

    cases = covid.get_status_of_one(slug_name)

    return render_template('__country_case.html' , name = country_name , cases = cases)

