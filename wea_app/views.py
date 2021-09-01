from django.shortcuts import render,HttpResponse
import requests
import time
import datetime
from .models import City
from.forms import CityForm


# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4defe20be9fb35451c4bdd6801bdc930'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    
    form = CityForm()

    cities = City.objects.all()

    weather_data = []
    #city = request.POST["inputcity"]

    for city in cities:
            
            r = requests.get(url.format(city)).json()
            
            result = {
                "lat" : r['coord']['lat'],
                "lon" : r['coord']['lon'],
            }
            mainurl = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,hourly&units=metric&appid=4defe20be9fb35451c4bdd6801bdc930'
            a = requests.get(mainurl.format(result['lat'],result['lon'])).json()



            mainresult = {
                "city":city.name,
                "temprature": round(a['current']['temp']),
                "description": a['current']['weather'][0]['description'].title(),
                "icons": r['weather'][0]['icon'],
                "feels": round(a['current']['feels_like'],1),
                "windspeed" :  a['current']['wind_speed'],
                "timezone" :  a['timezone'] ,
                "pressure" : a['current']['pressure'],
                "humidity" : a['current']['humidity'],
                "countrycode" : r['sys']['country'],
                "dt" : time.strftime("%I:%M %p",time.gmtime(a['current']['dt'] + a['timezone_offset'] )),
                "dtdate" : time.strftime("%A, %B %d, %Y",time.gmtime(a['current']['dt'] + a['timezone_offset'] )),
                "dtforecastdate1" : time.strftime("%a",time.gmtime(a['daily'][1]['dt'])),
                "dtforecastdate2" : time.strftime("%a",time.gmtime(a['daily'][2]['dt'])),
                "dtforecastdate3" : time.strftime("%a",time.gmtime(a['daily'][3]['dt'])),
                "dtforecastdate4" : time.strftime("%a",time.gmtime(a['daily'][4]['dt'])),
                "temprature1": round(a['daily'][1]['temp']['day']),
                "temprature2": round(a['daily'][2]['temp']['day']),
                "temprature3": round(a['daily'][3]['temp']['day']),
                "temprature4": round(a['daily'][4]['temp']['day']),
                "min1": round(a['daily'][1]['temp']['min']),
                "min2": round(a['daily'][2]['temp']['min']),
                "min3": round(a['daily'][3]['temp']['min']),
                "min4": round(a['daily'][4]['temp']['min']),
                "max1": round(a['daily'][1]['temp']['max']),
                "max2": round(a['daily'][2]['temp']['max']),
                "max3": round(a['daily'][3]['temp']['max']),
                "max4": round(a['daily'][4]['temp']['max']),
                "desc1": a['daily'][1]['weather'][0]['main'],
                "desc2": a['daily'][2]['weather'][0]['main'],
                "desc3": a['daily'][3]['weather'][0]['main'],
                "desc4": a['daily'][4]['weather'][0]['main'],
                "forecasticon1" : a['daily'][1]['weather'][0]['icon'],
                "forecasticon2" : a['daily'][2]['weather'][0]['icon'],
                "forecasticon3" : a['daily'][3]['weather'][0]['icon'],
                "forecasticon4" : a['daily'][4]['weather'][0]['icon'],

            }
            weather_data.append(mainresult)
    
    icon = mainresult['icons']
    context = {"weather_data":weather_data,"icon":icon,"form":form}
    return render(request,'wea_app/index.html',context)
# return render(request,'wea_app/index.html')



