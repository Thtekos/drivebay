# Adds cart_count to every template context automatically

def cart_count(request):
    if request.user.is_authenticated:
        count = request.user.cart_items.count()
    else:
        count = 0
    return {'cart_count': count}