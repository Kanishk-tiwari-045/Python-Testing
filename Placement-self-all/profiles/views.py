from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .models import Profile  # Assuming Profile is your model for LinkedIn profiles
from django.conf import settings
from django.contrib.auth import get_user_model
import requests

User = get_user_model()

def linkedin_login(request):
    linkedin_auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        "?response_type=code"
        f"&client_id={settings.LINKEDIN_CLIENT_ID}"
        f"&redirect_uri={settings.LINKEDIN_REDIRECT_URI}"
        "&scope=openid%20profile%20email"
    )
    return redirect(linkedin_auth_url)


def linkedin_callback(request):
    print("linkedin_callback view called")
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Authorization code is missing.", status=400)

    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    access_token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
        'client_id': settings.LINKEDIN_CLIENT_ID,
        'client_secret': settings.LINKEDIN_CLIENT_SECRET
    }
    access_token_response = requests.post(access_token_url, data=access_token_data)
    access_token_json = access_token_response.json()
    access_token = access_token_json.get('access_token')

    if not access_token:
        return HttpResponse("Failed to obtain access token from LinkedIn.", status=400)

    profile_url = 'https://api.linkedin.com/v2/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive'
    }
    profile_response = requests.get(profile_url, headers=headers)
    profile_data = profile_response.json()
    # Printing claims to the console
    claims_supported = ["sub", "name", "given_name", "family_name", "picture", "email", "email_verified", "locale"]
    print("Claims Supported:")
    for claim in claims_supported:
        print(f"{claim}: {profile_data.get(claim)}")

    first_name = profile_data.get('given_name')
    last_name = profile_data.get('family_name')
    email = profile_data.get('email')

    if not email:
        return HttpResponse("Email address is missing from LinkedIn profile.", status=400)

    try:
        linkedin_profile = Profile.objects.get(email=email)
        linkedin_profile.first_name = first_name
        linkedin_profile.last_name = last_name
        linkedin_profile.save()
    except Profile.DoesNotExist:
        user, created = User.objects.get_or_create(username=email, email=email)
        if created:
            linkedin_profile = Profile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            print("LinkedIn Profile saved successfully:", linkedin_profile.user.username)
        else:
            print("User already exists.")
    return HttpResponse("LinkedIn Profile saved successfully.")

def signup_view(request):
    return render(request, 'signup.html')
