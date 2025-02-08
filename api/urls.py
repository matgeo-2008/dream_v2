from django.urls import path
from . import main2

urlpatterns = [
    path('dream-interpretation/', main2.dream_interpretation, name='dream-interpretation'),
] 