import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import City
from .forms import CityForm

def index(request):
    appid = 'd225cc3fea16da6c212957b11a08a2ee'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if(request.method=='POST'):
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']

            existing_city = City.objects.filter(name=city_name).first()
            if not existing_city:
                form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon']
        }

        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)


def delete_city(request, city_name):
    city = get_object_or_404(City, name=city_name)
    if request.method == 'POST':
        city.delete()
        return redirect('index')



    return redirect('index')


