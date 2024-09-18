from django.conf import settings
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from rest_framework import status
from .models import Profile
import jwt
from math import radians, cos, sin, asin, sqrt

# Get User Data From DB
@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def getUserData(request):
    auth_header = request.headers.get('Authorization', None) # get user's access_token
    access_token = auth_header.split(' ')[1]  # Extract the token part
    decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = decoded_payload.get('user_id') # extract user_id from payload

    data = Profile.objects.filter(user_id=user_id).values() # get from db data where user_id=user_id

    return response.Response({'userData': data[0]}, status=status.HTTP_201_CREATED)


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def updateProfile(request):
    auth_header = request.headers.get('Authorization', None) # extract user's access_token
    access_token = auth_header.split(' ')[1]  # extract the token part
    decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = decoded_payload.get('user_id') # extract user_id from payload

    # Extract data
    age = request.data.get('age')
    gender = request.data.get('gender')
    location = request.data.get('location')
    images = request.data.get('images')
    interest = request.data.get('interest')
    bio = request.data.get('bio')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    # Update user's profile
    Profile.objects.filter(user_id=user_id).update(
        isFirstLogin=False,
        gender=gender,
        age=age,
        interested_in=interest,
        location=location,
        images=images,
        bio=bio,
        latitude=latitude,
        longitude=longitude
    )

    return response.Response(status=status.HTTP_201_CREATED)


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def modifyProfile(request):
    auth_header = request.headers.get('Authorization', None) # extract user's access_token
    access_token = auth_header.split(' ')[1]  # extract the token part
    decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = decoded_payload.get('user_id') # extract user_id from payload

    # Extract data
    age = request.data.get('age')
    ageRange = request.data.get('ageRange')
    bio = request.data.get('bio')
    distance = request.data.get('distance')
    gender = request.data.get('gender')
    images = request.data.get('images')
    interest = request.data.get('interested_in')
    location = request.data.get('location')

    # Update user's profile
    Profile.objects.filter(user_id=user_id).update(
            isFirstLogin=False,
            gender=gender, age=age,
            interested_in=interest,
            location=location,
            images=images,
            bio=bio,
            ageRange=ageRange,
            distance=distance
        )

    return response.Response(status=status.HTTP_201_CREATED)


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def fetchProfiles(request):
    auth_header = request.headers.get('Authorization', None) # extract user's access_token
    access_token = auth_header.split(' ')[1]  # extract the token part
    decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = decoded_payload.get('user_id') # extract user_id from payload

    # Extract data
    ageRange = request.data.get('ageRange') # match with age
    distance = request.data.get('distance') #
    interest = request.data.get('interest') # match with gender
    user_lat= request.data.get('latitude')
    user_lon = request.data.get('longitude')

    # Fetch the user's profile to get the blacklist
    profile = Profile.objects.get(user_id=user_id)
    user_blacklist = profile.blacklist
    
    # Add the current user ID to the blacklist to ensure they are excluded
    user_blacklist.append(user_id)

    # Filter profiles based on age range and interest
    min_age, max_age = ageRange

    profiles = Profile.objects.filter(age__gte=min_age, age__lte=max_age, gender=interest).exclude(user_id__in=user_blacklist)

    # Filter by distance
    matching_profiles = []
    for profile in profiles:
        profile_lat, profile_lon = profile.latitude, profile.longitude

        profile_distance = haversine(user_lon, user_lat, profile_lon, profile_lat)
        
        if profile_distance <= distance:  # only include profiles within the specified distance
            matching_profiles.append(profile)

    # Return the list of matching profiles
    profiles_data = [
        {
            'user_id': profile.user_id,
            'username': profile.user.username,
            'firstname': profile.first_name,
            'lastname': profile.user.last_name,
            'age': profile.age,
            'location': profile.location,
            'bio': profile.bio,
            'images': profile.images,
            'distance': haversine(user_lon, user_lat, profile.longitude, profile.latitude)
        }
        for profile in matching_profiles
    ]

    return response.Response({'usersProfilesData': profiles_data}, status=status.HTTP_200_OK)


@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def fetchOwnProfile(request):
    auth_header = request.headers.get('Authorization', None) # extract user's access_token
    access_token = auth_header.split(' ')[1]  # extract the token part
    decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = decoded_payload.get('user_id') # extract user_id from payload
    
    profile = Profile.objects.get(user_id=user_id)
    print(profile)

    # Assuming there's only one profile per user_id
    # profile = profile.first()

    # Return the list of matching profiles
    profile_data = [
            {
            'user_id': profile.user_id,
            'username': profile.user.username,
            'firstname': profile.first_name,
            'lastname': profile.user.last_name,
            'age': profile.age,
            'location': profile.location,
            'bio': profile.bio,
            'images': profile.images,
        }
    ]

    return response.Response({'usersProfileData': profile_data}, status=status.HTTP_200_OK)


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def handleUserReaction(request, action):
    auth_header = request.headers.get('Authorization', None)
    access_token = auth_header.split(' ')[1]
    decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = decoded_payload.get('user_id') # 4

    target_user_id = request.data.get('target_user_id')  # ID of user(if liked), 4 OR users(if disliked), [2,4,7]
    print('hodss', target_user_id)
    
    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return response.Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if action == 'like':    
        # Fetch the target_profile
        try:
            target_profile = Profile.objects.get(user_id=target_user_id)
        except Profile.DoesNotExist:
            return response.Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)  

        # Add target_user_id to user_id blacklist             
        if target_user_id not in profile.blacklist:
            profile.blacklist.append(target_user_id)

        likes = target_profile.likes
        if user_id not in likes:
            likes.append(user_id)
            target_profile.likes = likes

        target_profile.save()

    elif action == 'dislike':
        for id in target_user_id:
            # Add target_user_id to user_id blacklist             
            if id not in profile.blacklist:
                print('hod', id)
                profile.blacklist.append(id)
            

    # Save changes to the profile
    profile.save()

    return response.Response({'status': 'success'}, status=status.HTTP_200_OK)


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def verifyMatch(request):
    auth_header = request.headers.get('Authorization', None)
    access_token = auth_header.split(' ')[1]
    decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = decoded_payload.get('user_id')

    target_user_id = request.data.get('target_user_id')  # The ID of the user being liked/disliked 14

    # Fetch the profile
    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return response.Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    # Fetch the target_profile
    try:
        target_profile = Profile.objects.get(user_id=target_user_id)
    except Profile.DoesNotExist:
        return response.Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


    matches = profile.matches
    if target_user_id not in matches:
        matches.append(target_user_id)
        profile.matches = matches

    matches_two = target_profile.matches
    if user_id not in matches_two:
        matches_two.append(user_id)
        target_profile.matches = matches_two

        # Remove for each user the his likes in db - 'likes'
        profile.likes.remove(target_user_id)
        target_profile.likes.remove(user_id)

    # Save changes to the profile
    profile.save()
    # Save changes to the target_profile
    target_profile.save()
    
    return response.Response({'status': 'success'}, status=status.HTTP_200_OK)

# --------- Functions ---------

# Haversine formula to calculate the distance between two points
def haversine(lon1, lat1, lon2, lat2):
    # Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of Earth in kilometers. Use 3956 for miles. Determines return value units.
    km = 6371 * c
    return km
