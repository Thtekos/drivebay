from django.contrib import admin
from .models import Make, CarModel, Car, UserProfile, Review, CartItem, Wishlist, ViewHistory, Purchase


@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'make']
    search_fields = ['name', 'make__name']
    list_filter = ['make']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'fuel_type', 'transmission', 'condition', 'is_available', 'created_at']
    search_fields = ['make__name', 'car_model__name']
    list_filter = ['fuel_type', 'transmission', 'condition', 'is_available', 'make']
    list_editable = ['is_available']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'location']
    search_fields = ['user__username', 'user__email']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__username', 'car__make__name']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'added_at']
    search_fields = ['user__username']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'added_at']
    search_fields = ['user__username']


@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'viewed_at']
    search_fields = ['user__username']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'price_paid', 'purchased_at']
    search_fields = ['user__username']