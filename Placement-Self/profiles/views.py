from django.shortcuts import render, redirect
from django.conf import settings
from .models import Profile
from django.contrib.auth.decorators import login_required
import requests
import json

def linkedin_login(request):
    linkedin_auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        "?response_type=code"
        f"&client_id={settings.LINKEDIN_CLIENT_ID}"
        f"&redirect_uri={settings.LINKEDIN_REDIRECT_URI}"
        "&scope=openid%20profile%20email"
    )
    return redirect(linkedin_auth_url)

@login_required
def linkedin_callback(request):
    code = request.GET.get('code')
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
        'client_id': settings.LINKEDIN_CLIENT_ID,
        'client_secret': settings.LINKEDIN_CLIENT_SECRET,
    }
    response = requests.post(access_token_url, data=data)
    response.raise_for_status()
    response_data = response.json()
    access_token = response_data.get('access_token')
    id_token = response_data.get('id_token')
    print(f'Access Token: {access_token}')
    print(f'ID Token: {id_token}')
    user_info = fetch_linkedin_user_info(access_token)
    print(f'User Info: {json.dumps(user_info, indent=2)}')
    user = request.user
    save_linkedin_data(user_info, user)
    return render(request,'signup.html')

def fetch_linkedin_user_info(access_token):
    userinfo_url = 'https://api.linkedin.com/v2/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    userinfo_response = requests.get(userinfo_url, headers=headers)
    userinfo_response.raise_for_status()
    user_info = userinfo_response.json()
    return user_info

def save_linkedin_data(linkedin_data, user):
    email = linkedin_data.get('email', '')
    first_name = linkedin_data.get('localizedFirstName', '')
    last_name = linkedin_data.get('localizedLastName', '')
    profile_picture = linkedin_data.get('profilePicture', {}).get('displayImage', '')

    profile, created = Profile.objects.get_or_create(user=user)
    
    updated = False

    if profile.first_name != first_name:
        profile.first_name = first_name
        updated = True
    if profile.last_name != last_name:
        profile.last_name = last_name
        updated = True
    if profile.email != email:
        profile.email = email
        updated = True
    if profile.picture != profile_picture:
        profile.picture = profile_picture
        updated = True

    if updated or created:
        profile.save()
        print("Profile saved successfully.")
    else:
        print("Profile is up to date, no changes made.")

def signup_view(request):
    return render(request, 'signup.html')