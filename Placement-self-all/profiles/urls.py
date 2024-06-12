from django.urls import path
from .views import signup_view, linkedin_login, linkedin_callback

urlpatterns = [
    path('', signup_view, name='signup'),
    path('linkedin/login/', linkedin_login, name='linkedin_login'),
    path('linkedin/callback/', linkedin_callback, name='linkedin_callback'),
]
