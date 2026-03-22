from django.shortcuts import render, get_object_or_404
from .models import Car, Make, CarModel, ViewHistory

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


def car_list(request):
    cars = Car.objects.filter(is_available=True)
    makes = Make.objects.all()

    # Search by name or model
    query = request.GET.get('q', '')
    if query:
        cars = cars.filter(car_model__name__icontains=query) | cars.filter(make__name__icontains=query)

    # Filter by make
    make_id = request.GET.get('make', '')
    if make_id:
        cars = cars.filter(make__id=make_id)

    # Filter by fuel type
    fuel = request.GET.get('fuel', '')
    if fuel:
        cars = cars.filter(fuel_type=fuel)

    # Filter by transmission
    transmission = request.GET.get('transmission', '')
    if transmission:
        cars = cars.filter(transmission=transmission)

    # Filter by color
    color = request.GET.get('color', '')
    if color:
        cars = cars.filter(color=color)

    # Filter by condition
    condition = request.GET.get('condition', '')
    if condition:
        cars = cars.filter(condition=condition)

    # Filter by price range
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        cars = cars.filter(price__gte=min_price)
    if max_price:
        cars = cars.filter(price__lte=max_price)

    # Filter by year range
    min_year = request.GET.get('min_year', '')
    max_year = request.GET.get('max_year', '')
    if min_year:
        cars = cars.filter(year__gte=min_year)
    if max_year:
        cars = cars.filter(year__lte=max_year)

    # Filter by max mileage
    max_mileage = request.GET.get('max_mileage', '')
    if max_mileage:
        cars = cars.filter(mileage__lte=max_mileage)

    # Sorting
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = ['price', '-price', '-created_at', 'year', '-year', 'mileage']
    if sort in valid_sorts:
        cars = cars.order_by(sort)

    context = {
        'cars': cars,
        'makes': makes,
        'fuel_choices': Car.FUEL_CHOICES,
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'color_choices': Car.COLOR_CHOICES,
        'condition_choices': Car.CONDITION_CHOICES,
        'query': query,
        'selected_make': make_id,
        'selected_fuel': fuel,
        'selected_transmission': transmission,
        'selected_color': color,
        'selected_condition': condition,
        'min_price': min_price,
        'max_price': max_price,
        'min_year': min_year,
        'max_year': max_year,
        'max_mileage': max_mileage,
        'sort': sort,
        'total_results': cars.count(),
    }
    return render(request, 'car_list.html', context)


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_available=True)

    # Save view history for logged in users
    if request.user.is_authenticated:
        ViewHistory.objects.update_or_create(
            user=request.user,
            car=car,
        )

    # Similar cars for recommender (same make or fuel type)
    similar_cars = Car.objects.filter(
        is_available=True,
        make=car.make,
    ).exclude(id=car.id)[:4]

    # If not enough similar by make, fill with same fuel type
    if similar_cars.count() < 4:
        extra = Car.objects.filter(
            is_available=True,
            fuel_type=car.fuel_type,
        ).exclude(id=car.id).exclude(id__in=similar_cars)[:4 - similar_cars.count()]
        similar_cars = list(similar_cars) + list(extra)

    reviews = car.reviews.all()
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    car_specs = [
        {'icon': 'bi-calendar', 'label': 'Year', 'value': car.year},
        {'icon': 'bi-speedometer2', 'label': 'Mileage', 'value': f"{car.mileage:,} km"},
        {'icon': 'bi-fuel-pump', 'label': 'Fuel', 'value': car.get_fuel_type_display()},
        {'icon': 'bi-gear', 'label': 'Transmission', 'value': car.get_transmission_display()},
        {'icon': 'bi-palette', 'label': 'Color', 'value': car.get_color_display()},
        {'icon': 'bi-award', 'label': 'Condition', 'value': car.get_condition_display()},
    ]

    context = {
        'car': car,
        'car_specs': car_specs,
        'similar_cars': similar_cars,
        'reviews': reviews,
        'user_review': user_review,
        'rating_range': range(1, 6),
    }
    return render(request, 'car_detail.html', context)