from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.index, name = "index"),
    path('signup/', views.sign_up, name ='signup'),
    path("login/", views.user_login, name="login"),
    path("profile/", views.profile, name="profile"),
    path('logout/', views.logout_page, name='logout_page'),
    path('<int:pk>/workerdetails/', views.worker_details, name='worker_details'),
   
    path('clientprofile/', views.client_profile, name='client_profile'),
    path('worker/<int:pk>/', views.worker_profile, name='worker_profile'),
    path('client/<int:pk>/', views.client_profile, name='client_profile'),

    
]
