from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('api/aggregate/', views.ip_aggregator_api, name='ip_aggregator_api'),
    #path('', views.aggregator, name = 'aggregate'),
]
