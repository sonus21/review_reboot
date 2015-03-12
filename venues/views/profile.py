from django.shortcuts import render
from venues.models.restaurant import Restaurant
from venues.models.venue import Venue

__author__ = 'm'

def index(request):
    user_restaurants = Restaurant.objects.filter(created_by=request.user)
    modified_by_user_restaurants = Restaurant.objects.filter(modified_by=request.user)\
        .exclude(pk__in=user_restaurants)
    return render(request, "profile/index.html", {
        'user_restaurants': user_restaurants,
        'modified_by_user_restaurants': modified_by_user_restaurants,
    })