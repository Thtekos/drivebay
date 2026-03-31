from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Make, CarModel, ViewHistory, UserProfile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import admin_required, login_required_redirect
from django.db import models
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Car, Make, CarModel, ViewHistory, UserProfile, Review, CartItem, Wishlist


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
        try:
            cars = cars.filter(make__id=int(make_id))
        except ValueError:
            pass

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

def register_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        phone = request.POST.get('phone', '').strip()
        location = request.POST.get('location', '').strip()

        # Validation
        errors = []
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username is already taken.')
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email is already registered.')
        if len(password1) < 8:
            errors.append('Password must be at least 8 characters.')
        if password1 != password2:
            errors.append('Passwords do not match.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register.html', {'form_data': request.POST})

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )

        # Create profile
        UserProfile.objects.create(
            user=user,
            phone=phone,
            location=location,
        )

        login(request, user)
        messages.success(request, f'Welcome to DriveBay, {first_name or username}!')
        return redirect('home')

    return render(request, 'register.html', {})


def login_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'username': username})

    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required_redirect
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()

        # Update profile fields
        profile.phone = request.POST.get('phone', '').strip()
        profile.location = request.POST.get('location', '').strip()
        profile.bio = request.POST.get('bio', '').strip()

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)

@login_required_redirect
def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password', '')
        new_password1 = request.POST.get('new_password1', '')
        new_password2 = request.POST.get('new_password2', '')

        # Validate current password
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('profile')

        if len(new_password1) < 8:
            messages.error(request, 'New password must be at least 8 characters.')
            return redirect('profile')

        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('profile')

        request.user.set_password(new_password1)
        request.user.save()

        # Re-login after password change
        login(request, request.user)
        messages.success(request, 'Password updated successfully.')
        return redirect('profile')

    return redirect('profile')

@login_required_redirect
def dashboard_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Recently viewed cars
    view_history = ViewHistory.objects.filter(
        user=request.user
    ).select_related('car').order_by('-viewed_at')[:6]

    # Wishlist
    wishlist = request.user.wishlist.select_related('car').order_by('-added_at')[:6]

    # Purchases
    purchases = request.user.purchases.select_related('car').order_by('-purchased_at')[:6]

    # Reviews given
    reviews = request.user.reviews.select_related('car').order_by('-created_at')[:5]

    # Cart items
    cart_items = request.user.cart_items.select_related('car').order_by('-added_at')

    # Stats
    stats = {
        'viewed': ViewHistory.objects.filter(user=request.user).count(),
        'wishlist': request.user.wishlist.count(),
        'purchases': request.user.purchases.count(),
        'reviews': request.user.reviews.count(),
    }
    
    stats_list = [
        ('Cars Viewed', 'bi-clock-history', stats['viewed']),
        ('Wishlist', 'bi-heart', stats['wishlist']),
        ('Purchases', 'bi-bag-check', stats['purchases']),
        ('Reviews', 'bi-star', stats['reviews']),
    ]

    context = {
        'profile': profile,
        'view_history': view_history,
        'wishlist': wishlist,
        'purchases': purchases,
        'reviews': reviews,
        'cart_items': cart_items,
        'stats': stats,
        'stats_list': stats_list,
        'rating_range': range(1, 6),
    }
    return render(request, 'dashboard.html', context)

def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    results = []
    if len(query) >= 2:
        cars = Car.objects.filter(
            is_available=True
        ).filter(
            models.Q(make__name__icontains=query) |
            models.Q(car_model__name__icontains=query)
        ).values('id', 'make__name', 'car_model__name', 'year', 'price')[:6]

        for car in cars:
            results.append({
                'id': car['id'],
                'label': f"{car['year']} {car['make__name']} {car['car_model__name']}",
                'price': f"€{int(car['price']):,}",
            })
    return JsonResponse({'results': results})

@login_required_redirect
@require_POST
def submit_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Check if user already reviewed this car
    if Review.objects.filter(car=car, user=request.user).exists():
        return JsonResponse({'success': False, 'error': 'You have already reviewed this car.'})

    try:
        rating = int(request.POST.get('rating', 0))
        if rating < 1 or rating > 5:
            return JsonResponse({'success': False, 'error': 'Rating must be between 1 and 5.'})
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Invalid rating value.'})

    comment = request.POST.get('comment', '').strip()

    Review.objects.create(
        car=car,
        user=request.user,
        rating=rating,
        comment=comment,
    )

    return JsonResponse({
        'success': True,
        'message': 'Review submitted successfully.',
        'rating': rating,
        'username': request.user.username,
        'comment': comment,
    })
    
@login_required_redirect
def cart_view(request):
    cart_items = request.user.cart_items.select_related('car').order_by('-added_at')
    total = sum(item.car.price for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)


@login_required_redirect
@require_POST
def cart_add(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_available=True)

    # Check if already in cart
    if request.user.cart_items.filter(car=car).exists():
        return JsonResponse({'success': False, 'error': 'This car is already in your cart.'})

    CartItem.objects.create(user=request.user, car=car)
    cart_count = request.user.cart_items.count()
    return JsonResponse({'success': True, 'cart_count': cart_count})


@login_required_redirect
@require_POST
def cart_remove(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    request.user.cart_items.filter(car=car).delete()
    cart_count = request.user.cart_items.count()

    # Recalculate total
    cart_items = request.user.cart_items.select_related('car').all()
    total = sum(item.car.price for item in cart_items)

    return JsonResponse({
        'success': True,
        'cart_count': cart_count,
        'total': f"{total:,.0f}",
    })


@login_required_redirect
@require_POST
def cart_checkout(request):
    from .models import Purchase
    cart_items = request.user.cart_items.select_related('car').all()

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    # Simulate purchase for each cart item
    for item in cart_items:
        Purchase.objects.get_or_create(
            user=request.user,
            car=item.car,
            defaults={'price_paid': item.car.price},
        )
        # Mark car as unavailable
        item.car.is_available = False
        item.car.save()

    # Clear the cart
    request.user.cart_items.all().delete()
    messages.success(request, 'Purchase completed! Thank you for using DriveBay.')
    return redirect('dashboard')

@login_required_redirect
@require_POST
def wishlist_add(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.user.wishlist.filter(car=car).exists():
        return JsonResponse({'success': False, 'error': 'Already in your wishlist.'})

    Wishlist.objects.create(user=request.user, car=car)
    return JsonResponse({'success': True})


@login_required_redirect
@require_POST
def wishlist_remove(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    request.user.wishlist.filter(car=car).delete()
    return JsonResponse({'success': True})