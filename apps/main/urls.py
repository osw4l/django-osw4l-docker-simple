from django.urls import include, path
from .views import landing

urlpatterns = [
    path('landing/', landing),

]
