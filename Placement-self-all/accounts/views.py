from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,HTTP_200_OK
from .serializers import UserSignUpSerializer, UserSignInSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.http import HttpResponse

# from django.views.generic.edit import CreateView

User = get_user_model()

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_401_UNAUTHORIZED)



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponse("Redirected to home page")  # Redirect to a success page
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
    # return HttpResponse("HELLLLLLLLLLLLLLLLLLLLLLLO")
