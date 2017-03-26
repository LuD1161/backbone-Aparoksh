# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render
import requests, json
from pprint import pprint

zomato_api_key = '679e43e313e29572b8880fb59d1492cf'
url = "https://developers.zomato.com/api/v2.1/"
fields = {'location': 'locations?query=', 'cuisine': 'cuisines?city_id=',
          'restaurant': 'restaurant?res_id=', 'review': 'reviews?res_id=21',
          'search': 'search?entity_id='}

def home(request):
	return render(request,'home.html')

def Restprint(location, query=None):
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": zomato_api_key}
    url = "https://developers.zomato.com/api/v2.1/" + str(fields['location']) + location

    response = requests.get(url, proxies={'https': "https://rit2015044:Iiita015@172.31.1.6:8080"}, headers=header)
    restJSON = response.json()
    if (restJSON['status'] != 'success'):
        return "Sorry No place found to your description"
    id = restJSON['location_suggestions'][0]['entity_id']
    finalURL = url + str(fields['search']) + str(id) + 'q=' + query+"&order=desc"
    response = requests.get(finalURL, proxies={'https': "https://rit2015044:Iiita015@172.31.1.6:8080"}, headers=header)

    restJSON = response.json()
    print(restJson)
    return render(request,'food.html')
    # for restaurant in restJSON['best_rated_restaurant']:
    #     text = "Name of Restaurant : " + restaurant['restaurant']['name'] + "\n"
    #     text = text + "User Ratings : " + restaurant['restaurant']['user_rating']['rating_text'] + "\n"
    #     text = text + "Available Cuisines : " + restaurant['restaurant']['cuisines'] + "\n"
    #     text = text + restaurant['restaurant']['featured_image'] + "\n"
    #     text = text + "Address : " + restaurant['restaurant']['location']['address'] + "\n"
    #     text = text + "Menu Link :" + restaurant['restaurant']['menu_url'] + "\n"
    #     text = text.encode("utf-8")
    #     if (restaurant['restaurant']['average_cost_for_two'] <= 0):
    #         restaurant['restaurant']['average_cost_for_two'] = "Unavailable"
    #     text = text + "Average Cost for two people : ₹ " + str(restaurant['restaurant']['average_cost_for_two']) + "\n"
    #     print text


# Restprint("Allahabad")


def food(request):
    place = request.POST.get('place')
    print place
    cuisine = request.POST.get('cuisine', None)
    restaurant = request.POST.get('restaurant', None)
    query = str(restaurant)+str(cuisine)
    return HttpResponse(Restprint(place, query), content_type="application/json")