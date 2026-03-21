from django.shortcuts import render
from .models import Car, Make

def home(request):
    featured_cars = Car.objects.filter(is_available=True)[:8]
    makes = Make.objects.all()
    why_items = [
        {'icon': 'bi-shield-check', 'title': 'Verified Listings', 'desc': 'Every listing is reviewed before going live.'},
        {'icon': 'bi-cash-coin', 'title': 'Best Prices', 'desc': 'Compare thousands of cars and find the best deal.'},
        {'icon': 'bi-headset', 'title': '24/7 Support', 'desc': 'Our team is always here to help you find your car.'},
    ]
    context = {
        'featured_cars': featured_cars,
        'makes': makes,
        'why_items': why_items,
    }
    return render(request, 'home.html', context)