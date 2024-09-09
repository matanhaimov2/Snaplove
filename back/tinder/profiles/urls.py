from django.urls import path
from .views import getUserData, updateProfile, modifyProfile

urlpatterns = [
    path("getUserData/", getUserData, name='getUserData'),
    path("updateProfile/", updateProfile, name='updateProfile'),
    path("modifyProfile/", modifyProfile, name='modifyProfile'),

]