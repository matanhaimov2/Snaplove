from django.urls import path
from .views import getUserData, updateProfile, modifyProfile, fetchProfiles, fetchOwnProfile, handleUserReaction, verifyMatch

urlpatterns = [
    path("getUserData/", getUserData, name='getUserData'),
    path("updateProfile/", updateProfile, name='updateProfile'),
    path("modifyProfile/", modifyProfile, name='modifyProfile'),
    path("fetchProfiles/", fetchProfiles, name='fetchProfiles'),
    path("fetchOwnProfile/", fetchOwnProfile, name='fetchOwnProfile'),
    path("userAction/<str:action>/", handleUserReaction, name="handleUserReaction"),
    path("verifyMatch/", verifyMatch, name="verifyMatch"),
]