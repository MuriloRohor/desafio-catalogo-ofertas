from django.urls import path
from catalogo import views

urlpatterns = [
    path('produto/', views.produto, name='produto'),
    path('buscar-produtos/', views.scrape_products, name='scrape_products')
]
