import requests
import json

class Covid:
    def __init__(self) -> None:
        self.summary_url = 'https://api.covid19api.com/summary'
        self.status_url = 'https://api.covid19api.com/country/{}'
    
    def get_summary_cases(self) -> dict:
        self.cases = {}

        res = requests.get(self.summary_url).json()

        try:
            cases = res['Global']
        except:
            return None
        
        headers = ['New Confirmed' , 'Total Confirmed' , 'New Deaths' , 'Total Deaths' , 'New Recovered' , 'Total Recovered']

        for key , value in zip(headers , list(cases.values())[:-1]):
            self.cases[key] = value
        
        return self.cases
    
    def get_countries(self):
        res = requests.get('https://api.covid19api.com/countries').json()

        self.countries = {}

        for response in res:
            self.countries[response["Country"]] = response["Slug"]
        
        return dict(sorted(self.countries.items() , key=lambda x: x[1]))

    def get_status_of_one(self , slug_name) -> dict:
        res = requests.get(self.status_url.format(slug_name)).json()[-1]

        self.cases = {}

        for i in ['Confirmed' , 'Deaths' , 'Recovered' , 'Active']:
            self.cases[i] = res[i]
        
        return self.cases