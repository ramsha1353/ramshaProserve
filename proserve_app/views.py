from django.shortcuts import render, redirect,get_object_or_404
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth. forms import AuthenticationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile, WorkerProfile
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.core.paginator import Paginator

# registration

def sign_up(request):
        if request.method =='POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                messages.success(request, ("Registered Succesfull !!!"))
                
                user, user_profile = form.save()
                login(request, user)
                return redirect('login') 
        else:
            form = SignUpForm()
        return render(request, 'registration.html', {'form': form})
    
               
            
# login

def user_login (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        form = user.userprofile
        user_type = user.userprofile.user_type
        print(user_type)
        if user_type == 'worker':
           
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in succesfully !!')
                

            return HttpResponseRedirect(reverse('worker_details', args=[user.userprofile.pk]))

        elif user_type == 'customer':
            if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in succesfully !!')
            return HttpResponseRedirect(reverse('client_profile', args=[user.userprofile.pk]))
        
       
    else:
        form=AuthenticationForm()
        return render(request, 'login.html',{'form':form})



# def profile(request):
#     return render(request, 'profile.html')
@login_required(login_url="/index")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

    # return HttpResponseRedirect(reverse("login"))
    
   
def index(request):
    return render (request, "index.html")
    
@login_required(login_url="/index")
def worker_profile(request, pk):
    # if request.user.is_authenticated:


       
    user_profile = get_object_or_404(UserProfile, pk=pk)
    user_type = user_profile.user_type
    
    if user_type == 'customer':
        return render(request, "worker_lists.html",{
                    "error_message": "This is a customer id"
                    })
    elif request.method == 'GET':
        work_profile = WorkerProfile.objects.filter(profile=user_profile)
        return render(request, "worker_profile.html", {"user_profile": user_profile,  "work_profile": work_profile})
    elif request.method == 'POST':
        service = request.POST["service"]
        price_per_day = request.POST["price_per_day"]
        description = request.POST["description"]
        experiance = request.POST["experiance"]
        available_time = request.POST["available_time"]
       
        if not service:
            return render(request, "worker_profile.html", {
                "user_profile": user_profile,
                "error_message": "Please enter a valid service"
            })
        
        # Check if the worker has already created 5 services
        existing_services_count = WorkerProfile.objects.filter(profile=user_profile).count()
        if existing_services_count >= 5:
            return render(request, "worker_profile.html", {
                "user_profile": user_profile,
                "error_message": "You have reached the maximum limit of services"
            })
        
        new_details = WorkerProfile(
            profile=user_profile,
            service=service,
            price_per_day=price_per_day,
            description=description,
            experiance=experiance,
            available_time=available_time
        )
        new_details.save()
        
        return HttpResponseRedirect(reverse("worker_details", args=(user_profile.id,)))

        # return render (request, "index.html")


        
        

        
        
@login_required(login_url="/index")
def worker_details(request, pk):
    
    # if request.user.is_authenticated:
  
    user_profile = get_object_or_404(UserProfile, pk=pk)
    work_profile = WorkerProfile.objects.filter(profile=user_profile)
    username = [profile.profile.user.username for profile in work_profile]
    return render(request, "worker_details.html", {"work_profile": work_profile, "username": username})
    #     work_profile = WorkerProfile.objects.get(profile=user_profile)
    #     username = work_profile.profile.user.username
    #     return render(request, "worker_details.html", {"work_profile": work_profile, "username": username})
    # except WorkerProfile.DoesNotExist:
    #     return HttpResponseRedirect(reverse('worker_profile', args=[user_profile.pk]))
       
       
        # user_type = work_profile.profile.user_type
    
        # if user_type == 'customer':
        #         return render(request, "worker_lists.html",)
        # else:
        #     username = work_profile.profile.user.username
        # return render(request, "worker_details.html", {"work_profile": work_profile, "username": username})
    # return render (request, "index.html")
            

@login_required(login_url="/index")
def client_profile(request, pk):
   
        user_profile = get_object_or_404(UserProfile, pk=pk)
        workers = WorkerProfile.objects.all()
        search_query = request.GET.get('service_search')

        # divide the services into multiple pages 
        paginator = Paginator(workers, 5)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        if search_query:
            workers = workers.filter(Q(service__icontains=search_query))
        return render(request, "client_profile.html", {"user_profile": user_profile, "workers": workers})


#  dispaly all services of all workers 
def workerlists(request):
    workers = WorkerProfile.objects.all()
    paginator = Paginator(workers, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    search_query = request.GET.get('service_search')
    if search_query:
        workers = workers.filter(Q(service__icontains=search_query))
    return render(request, "worker_lists.html", { "workers": workers, "page_obj": page_obj})

    
    


def about(request):
    return HttpResponse("This is about page")

def contactus(request):
    return HttpResponse("this is contact us page")

