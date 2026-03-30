from django.urls import path
from . import views

urlpatterns = [
    path('', views.management_dashboard, name='management_dashboard'),
    path('cars/', views.management_cars, name='management_cars'),
    path('cars/add/', views.management_car_add, name='management_car_add'),
    path('cars/<int:car_id>/edit/', views.management_car_edit, name='management_car_edit'),
    path('cars/<int:car_id>/delete/', views.management_car_delete, name='management_car_delete'),
    path('categories/', views.management_categories, name='management_categories'),
    path('categories/make/add/', views.management_make_add, name='management_make_add'),
    path('categories/make/<int:make_id>/delete/', views.management_make_delete, name='management_make_delete'),
    path('categories/model/add/', views.management_model_add, name='management_model_add'),
    path('categories/model/<int:model_id>/delete/', views.management_model_delete, name='management_model_delete'),
    path('users/', views.management_users, name='management_users'),
    path('users/<int:user_id>/toggle/', views.management_user_toggle, name='management_user_toggle'),
]