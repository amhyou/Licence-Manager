from django.urls import path
from .views import check, add

urlpatterns = [
    path('check', check),
    path('add', add),
]
