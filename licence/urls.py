from django.urls import path
from .views import check_licence

urlpatterns = [
    path('check', check_licence, name="check-licence"),
]
