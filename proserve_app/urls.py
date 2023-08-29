from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.index, name = "index"),
    path('signup/', views.sign_up, name ='signup'),
    path('about/', views.about, name ='about'),
    path('contactus/', views.contactus, name ='contactus'),
    path("login/", views.user_login, name="login"),
    path('workerlists/', views.workerlists, name='workerlists'),
    path('logout/', views.user_logout, name='user_logout'),
    
    path('<int:pk>/workerdetails/', views.worker_details, name='worker_details'),
   path('worker/service/<int:pk>/update/', views.update_worker_service, name='update_worker_service'),
   path('worker/service/<int:pk>/delete/', views.delete, name='delete'),
    path('clientprofile/', views.client_profile, name='client_profile'),
    path('worker/<int:pk>/', views.worker_profile, name='worker_profile'),
    path('client/<int:pk>/', views.client_profile, name='client_profile'),

    
]
