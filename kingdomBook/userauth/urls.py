from django.urls import path
from userauth import views


app_name ='userauth'

urlpatterns = [
    path('signup/', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('signout/', views.signOut, name='signout'),
    
    path('profile/update/', views.updateProfile, name='update-profile'),
]