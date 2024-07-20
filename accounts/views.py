from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from .forms import CustomUserCreationForm ,  CustomAuthenticationForm
from django.views import View


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})
# Create your views here.
