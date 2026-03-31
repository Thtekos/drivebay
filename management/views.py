from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Avg
from cars.models import Car, Make, CarModel, Review
from cars.decorators import admin_required
from django.contrib.auth.models import User


@admin_required
def management_dashboard(request):
    # Stats
    stats = {
        'total_cars': Car.objects.count(),
        'available_cars': Car.objects.filter(is_available=True).count(),
        'total_users': User.objects.filter(is_staff=False).count(),
        'total_reviews': Review.objects.count(),
        'makes': Make.objects.count(),
    }

    # Recent listings
    recent_cars = Car.objects.select_related('make', 'car_model').order_by('-created_at')[:5]

    # Recent users
    recent_users = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]

    context = {
        'stats': stats,
        'recent_cars': recent_cars,
        'recent_users': recent_users,
    }
    return render(request, 'management/dashboard.html', context)


@admin_required
def management_cars(request):
    cars = Car.objects.select_related('make', 'car_model').order_by('-created_at')

    # Search
    query = request.GET.get('q', '')
    if query:
        cars = cars.filter(
            make__name__icontains=query
        ) | cars.filter(
            car_model__name__icontains=query
        )

    context = {
        'cars': cars,
        'query': query,
        'total': cars.count(),
    }
    return render(request, 'management/cars.html', context)


@admin_required
def management_car_add(request):
    makes = Make.objects.all()
    car_models = CarModel.objects.select_related('make').all()

    if request.method == 'POST':
        errors = validate_car_form(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'management/car_form.html', {
                'makes': makes,
                'car_models': car_models,
                'fuel_choices': Car.FUEL_CHOICES,
                'transmission_choices': Car.TRANSMISSION_CHOICES,
                'color_choices': Car.COLOR_CHOICES,
                'condition_choices': Car.CONDITION_CHOICES,
                'action': 'Add',
                'form_data': {},
            })

        car = Car(
            make_id=request.POST.get('make'),
            car_model_id=request.POST.get('car_model'),
            year=request.POST.get('year'),
            price=request.POST.get('price'),
            mileage=request.POST.get('mileage'),
            fuel_type=request.POST.get('fuel_type'),
            transmission=request.POST.get('transmission'),
            color=request.POST.get('color'),
            condition=request.POST.get('condition'),
            description=request.POST.get('description', ''),
            is_available=request.POST.get('is_available') == 'on',
        )
        if 'image' in request.FILES:
            car.image = request.FILES['image']
        car.save()
        messages.success(request, f'Car "{car}" added successfully.')
        return redirect('management_cars')

    return render(request, 'management/car_form.html', {
        'makes': makes,
        'car_models': car_models,
        'fuel_choices': Car.FUEL_CHOICES,
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'color_choices': Car.COLOR_CHOICES,
        'condition_choices': Car.CONDITION_CHOICES,
        'action': 'Add',
    })


@admin_required
def management_car_edit(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    makes = Make.objects.all()
    car_models = CarModel.objects.select_related('make').all()

    if request.method == 'POST':
        errors = validate_car_form(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'management/car_form.html', {
                'car': car,
                'makes': makes,
                'car_models': car_models,
                'fuel_choices': Car.FUEL_CHOICES,
                'transmission_choices': Car.TRANSMISSION_CHOICES,
                'color_choices': Car.COLOR_CHOICES,
                'condition_choices': Car.CONDITION_CHOICES,
                'action': 'Edit',
                'form_data': {},
            })

        car.make_id = request.POST.get('make')
        car.car_model_id = request.POST.get('car_model')
        car.year = request.POST.get('year')
        car.price = request.POST.get('price')
        car.mileage = request.POST.get('mileage')
        car.fuel_type = request.POST.get('fuel_type')
        car.transmission = request.POST.get('transmission')
        car.color = request.POST.get('color')
        car.condition = request.POST.get('condition')
        car.description = request.POST.get('description', '')
        car.is_available = request.POST.get('is_available') == 'on'
        if 'image' in request.FILES:
            car.image = request.FILES['image']
        car.save()
        messages.success(request, f'Car "{car}" updated successfully.')
        return redirect('management_cars')

    return render(request, 'management/car_form.html', {
        'car': car,
        'makes': makes,
        'car_models': car_models,
        'fuel_choices': Car.FUEL_CHOICES,
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'color_choices': Car.COLOR_CHOICES,
        'condition_choices': Car.CONDITION_CHOICES,
        'action': 'Edit',
    })


@admin_required
def management_car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car_name = str(car)
        car.delete()
        messages.success(request, f'Car "{car_name}" deleted successfully.')
    return redirect('management_cars')


@admin_required
def management_categories(request):
    makes = Make.objects.annotate(car_count=Count('cars')).order_by('name')
    car_models = CarModel.objects.select_related('make').annotate(
        car_count=Count('cars')
    ).order_by('make__name', 'name')

    context = {
        'makes': makes,
        'car_models': car_models,
    }
    return render(request, 'management/categories.html', context)


@admin_required
def management_make_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        country = request.POST.get('country', '').strip()
        if not name:
            messages.error(request, 'Brand name is required.')
            return redirect('management_categories')
        if Make.objects.filter(name__iexact=name).exists():
            messages.error(request, f'Brand "{name}" already exists.')
            return redirect('management_categories')
        make = Make(name=name, country=country)
        if 'logo' in request.FILES:
            make.logo = request.FILES['logo']
        make.save()
        messages.success(request, f'Brand "{name}" added successfully.')
    return redirect('management_categories')


@admin_required
def management_make_delete(request, make_id):
    make = get_object_or_404(Make, id=make_id)
    if request.method == 'POST':
        make_name = make.name
        make.delete()
        messages.success(request, f'Brand "{make_name}" deleted.')
    return redirect('management_categories')


@admin_required
def management_model_add(request):
    if request.method == 'POST':
        make_id = request.POST.get('make')
        name = request.POST.get('name', '').strip()
        if not make_id or not name:
            messages.error(request, 'Brand and model name are required.')
            return redirect('management_categories')
        if CarModel.objects.filter(make_id=make_id, name__iexact=name).exists():
            messages.error(request, f'Model "{name}" already exists for this brand.')
            return redirect('management_categories')
        CarModel.objects.create(make_id=make_id, name=name)
        messages.success(request, f'Model "{name}" added successfully.')
    return redirect('management_categories')


@admin_required
def management_model_delete(request, model_id):
    car_model = get_object_or_404(CarModel, id=model_id)
    if request.method == 'POST':
        model_name = str(car_model)
        car_model.delete()
        messages.success(request, f'Model "{model_name}" deleted.')
    return redirect('management_categories')


@admin_required
def management_users(request):
    users = User.objects.filter(is_staff=False).select_related('profile').order_by('-date_joined')

    query = request.GET.get('q', '')
    if query:
        users = users.filter(username__icontains=query) | users.filter(email__icontains=query)

    context = {
        'users': users,
        'query': query,
        'total': users.count(),
    }
    return render(request, 'management/users.html', context)


@admin_required
def management_user_toggle(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User "{user.username}" {status}.')
    return redirect('management_users')


# Helper: validate car form fields
def validate_car_form(data):
    errors = []
    if not data.get('make'):
        errors.append('Brand is required.')
    if not data.get('car_model'):
        errors.append('Model is required.')
    try:
        year = int(data.get('year', 0))
        if year < 1990 or year > 2025:
            errors.append('Year must be between 1990 and 2025.')
    except ValueError:
        errors.append('Year must be a valid number.')
    try:
        price = float(data.get('price', 0))
        if price <= 0:
            errors.append('Price must be greater than 0.')
    except ValueError:
        errors.append('Price must be a valid number.')
    try:
        mileage = int(data.get('mileage', 0))
        if mileage < 0:
            errors.append('Mileage cannot be negative.')
    except ValueError:
        errors.append('Mileage must be a valid number.')
    return errors