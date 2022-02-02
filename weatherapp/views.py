from pprint import pprint

#! pprint daha iyi bir şekilde veriyi görüntüler.
import requests
from decouple import config
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import City


# Create your views here.
def index(request):
    cities = City.objects.all()
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric&lang=tr"
    # city = "London"
    key = config("API_KEY")
    # response = requests.get(url.format(city, key))
    # content = response.json()
    # pprint(content)
    # print(type(content))  # ! <class 'dict'>
    u_city = request.GET.get("city")
    # ! .get ile city'e ulaşıyoruz. böyle bir key yoksa none döner.
    # print(u_city)
    if u_city:
        response = requests.get(url.format(u_city, key))
        print(response.status_code)
        if response.status_code == 200:
            content = response.json()
            r_city = content["name"]
            if City.objects.filter(name=r_city):
                messages.warning(request, "City already exists")
            else:
                City.objects.create(name=r_city)
                messages.success(request, "City added successfully")
        else:
            messages.warning(request, "City not found")
        return redirect("home")
    city_data = []
    for city in cities:
        response = requests.get(url.format(city, key))
        content = response.json()
        # pprint(content)
        data = {
            "city": city,
            "temperature": content["main"]["temp"],
            "desc": content["weather"][0]["description"],
            "icon": content["weather"][0]["icon"],
        }
        city_data.append(data)
        # print(city_data)
        context = {
            "city_data": city_data,
        }

    return render(request, "weatherapp/index.html", context)


def deleteCity(request, city_id):
    # city = City.objects.get(id=city_id)
    # ! tyr except kullanmadan bu şekilde yazabiliriz. Crash olmaz.
    city = get_object_or_404(City, id=city_id)
    city.delete()
    messages.success(request, "City deleted successfully")
    return redirect("home")
