from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login

from .forms import RegisterForm

# ---------- Log-in and Regiester --------------

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatically log in the user
            return redirect('home')  # redirect to home page or any other page
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

