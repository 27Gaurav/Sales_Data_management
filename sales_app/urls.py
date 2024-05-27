from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_record, name='add_record'),
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),  # Add this line for products view
    path('regions/', views.regions, name='regions'),  
]
