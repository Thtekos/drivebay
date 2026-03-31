from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/<int:car_id>/review/', views.submit_review, name='submit_review'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:car_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:car_id>/', views.cart_remove, name='cart_remove'),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
    path('wishlist/add/<int:car_id>/', views.wishlist_add, name='wishlist_add'),
    path('wishlist/remove/<int:car_id>/', views.wishlist_remove, name='wishlist_remove'),
]