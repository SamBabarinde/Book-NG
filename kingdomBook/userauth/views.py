from django.shortcuts import render, redirect
from userauth.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from userauth.models import User, Profile


def signUp(request):
    form = UserRegisterForm
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hi {username}, welcome to BookNG, please confirm your email")
            user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
                                    )
            login(request, user)
            return redirect('core:index')
                
    else:
        print ('Something went wrong, please cheeck your details and try again!') 
        form = UserRegisterForm()  
    
    context = {
        'form': form,
        
    }
    return render(request, 'userauth/signup.html', context)


def signIn(request):
    # if request.user.is_authenticated:
    #     messages.warning(request, "can't access page, you're logged in already")
    #     return redirect('core:index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Hi {user.username}, you've been logged in")
                return redirect('core:index')
            
            else:
                messages.warning(request, f"There is an error, please check your details.")
                
        except:
            messages.warning(request, f"user with {email} does not exist")    
            
    context = {
            
        }
    
    return render(request, 'userauth/signin.html', context)


def signOut(request):
    logout(request)
    messages.success(request, "You are logged out")
    
    return render(request, 'core/index.html')


def updateProfile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile_save = form.save(commit=False)
            profile_save.user = request.user
            profile_save.save()
            messages.success(request, "changes saved successfully")
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)
        messages.error(request, "there was a problem please try again")
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'userauth/update-profile.html', context)