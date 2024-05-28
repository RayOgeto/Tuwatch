from django.urls import path
from .views import movie_list
from .views import search_results
from . import views

urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('search/', views.search_results, name='search_results'),
    path('search/', search_results, name='search_results')
]
