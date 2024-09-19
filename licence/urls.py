from django.urls import path
from .views import check_licence, add_licence

urlpatterns = [
    path('check', check_licence),
    path('add', add_licence),
]
