from django.shortcuts import render, redirect,get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import SignUpForm, worker_profileform
from django.contrib import messages
from django.contrib.auth. forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile, WorkerProfile
from django.contrib.auth.views import LoginView
from django.db.models import Q


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
            # if user_type=='worker':
            #     service = form.cleaned_data.get('service')
            #     description = form.cleaned_data.get('description')
            #     price = form.cleaned_data.get('price')
            #     price_per_day = form.cleaned_data.get('price_per_day')
            #     available_time = form.cleaned_data.get('available_time')
            #     WorkerProfile.objects.create(profile=profile, service=service, description=description, price=price, price_per_day=price_per_day, available_time=available_time)
            # else:
            #     ClientProfile.objects.create(profile=profile)
            
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



def profile(request):
    return render(request, 'profile.html')

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login/')

   
def index(request):
    return render (request, "index.html")
    

def worker_profile(request, pk):

    user_profile = get_object_or_404(UserProfile, pk=pk)
    user_type = user_profile.user_type
    print(user_type)
    if user_type == 'customer':
        return render(request, "worker_lists.html",{
                      "error_message": "This is a customer id"
                     } )
    elif request.method == 'GET':
        return render(request, "worker_profile.html", {"user_profile": user_profile})
    elif request.method == 'POST':
        service = request.POST["service"]
        price_per_day = request.POST["price_per_day"]
        if not service:
            return render(request, "worker_profile.html", {
                "user_profile": user_profile,
                "error_message": "Please enter a valid details"
            })
        
        new_details = WorkerProfile(
            user=user_profile,
            service=service,
            price_per_day=price_per_day

        )
        new_details.save()
        
       
        return HttpResponseRedirect(reverse("worker_details", args=(user_profile.id,)))
      
def worker_details(request, pk):
   work_profile = get_object_or_404(WorkerProfile, profile__pk=pk)
   user_type = work_profile.profile.user_type
   
   print(user_type)
   if user_type == 'customer':
        return render(request, "worker_lists.html",)
   else:
       username = work_profile.profile.user.username
   return render(request, "worker_details.html", {"work_profile": work_profile, "username": username})
        


def client_profile(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    workers = WorkerProfile.objects.all()
    search_query = request.GET.get('service_search')
    if search_query:
        workers = workers.filter(Q(service__icontains=search_query))
    return render(request, "client_profile.html", {"user_profile": user_profile, "workers": workers})

def about(request):
    return HttpResponse("This is about page")

def contactus(request):
    return HttpResponse("this is contact us page")

def workerlists(request):
    # user_profile = get_object_or_404(UserProfile, pk=pk)
    workers = WorkerProfile.objects.all()
    search_query = request.GET.get('service_search')
    if search_query:
        workers = workers.filter(Q(service__icontains=search_query))
    return render(request, "worker_lists.html", { "workers": workers,})

    
    



class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('profile_redirect')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sign_up'] = sign_up()
        return context
    
# def profile_redirect(request):
#     user = request.user
#     if user.is_authenticated:
#         user_type = user.userprofile.user_type
#         if user_type == 'worker':
#             return HttpResponseRedirect(reverse('worker_profile', args=[user.userprofile.pk]))
#         elif user_type == 'client':
#             return HttpResponseRedirect(reverse('client_profile', args=[user.userprofile.pk]))
#     return redirect('login')  # Redirect to login if user is not authenticated