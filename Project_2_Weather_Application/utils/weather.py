import requests

class Weather:
    def __init__(self) -> None:
        self.api_keys = ['6598ec17303ce87eb9cc1ca781926a3e' , 'd5eaef10fee0aac62b3e1018801c60ef' , '1059abf4a6e4fe6a3a13276817deac1f' , '8a83a98c53a9c1670f6887594e8f0c9c' , '5a5c6bcd82454efe40d020e972b682ba' , 'db71f7fbc4a376fcf09eaec1ad5261f9' , 'a11260a2cfe99b2b1cba6a20d14c05aa']
        
        self.request_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    
    def get_info(self , city_name):
        res = requests.get(self.request_url.format(city_name , self.api_keys[0]))
        
        if(res.status_code != 200): return None
        
        res = res.json()
        
        values = [
            res['name'] + ', ' + res['sys']['country'],
            round(res['main']['temp'] - 273),
            round(res['main']['feels_like'] - 273),
            self.title(res['weather'][0]['description']),
            round(res['main']['humidity']),
            round(res['wind']['speed']),
            round(res['main']['pressure']),
            round(res['visibility']) / 1000,
            self.get_icon_name(int(res['weather'][0]['id']))
        ]
        
        return values
    
    def title(self , name: list[str]):
        ans = []
        
        for i in name.split():
            ans.append(i.title())
        
        return " ".join(ans)
    
    def get_icon_name(self , id_name):
        if(id_name in range(200 , 233)):
            return 'thunderstorm'
        elif(id_name in range(300 , 322)):
            return 'cloud-drizzle'
        elif(id_name == 511 or id_name in range(600 , 623)):
            return 'snowflakes'
        elif(id_name in range(801 , 805)):
            return 'clouds'
        
        self.weather_icons = {
            701: 'fog',
            711: 'smoke',
            721: 'sun-haze',
            731: 'sun-dust',
            741: 'fog',
            751: 'sun-haz',
            762: 'volcano',
            771: 'wind',
            781: 'tornado'
        }
        
        try:
            return self.weather_icons[id_name]
        except:
            return "sun"