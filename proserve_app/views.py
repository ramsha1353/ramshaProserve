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
    # return render (request, "registration.html")
    return HttpResponse('this is index page ')

def worker_profile(request, pk):

    user_profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'GET':
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
        
        # return redirect('worker_details')
        return HttpResponseRedirect(reverse("worker_details", args=(user_profile.id,)))
    #     form = worker_profileform(request.POST, instance=worker_profile)
    #     if form.is_valid():
    #         worker_profile = form.save(commit=False)
    #         worker_profile.user = user_profile
    #         worker_profile.save()
    #         messages.success(request, "Details saved successfully!")
    #         return redirect('/worker_details/')
    # else:
    #     form = worker_profileform(instance=worker_profile)

    # return render(request, 'worker_profile.html', {'form': form})
    # user_profile = get_object_or_404(UserProfile, pk=pk)
    # 
    # print(user_profile)
    # if request.method == 'POST':
    #     form = worker_profileform(request.POST, instance=user_profile)
    #     print(form)
    #     if form.is_valid():
    #         form.save()
    #         print('sucessful')
    #         messages.success(request, "Details saved successfully!")
    #         return redirect('worker_details')
    # else:
    #     form = worker_profileform(instance=user_profile)

    # return render(request, 'worker_profile.html', {'form': form})
    
    # return render(request, 'worker_profile.html', {'user_profile': user_profile})
    # return render(request, 'worker_profile.html')
def worker_details(request, pk):
   work_profile = get_object_or_404(WorkerProfile, profile__pk=pk)
   print("Profile ID:", pk)
   print("UserProfile:", work_profile.profile)
   print("User:", work_profile.profile.user)
   print("Username:", work_profile.profile.user.username)
   username = work_profile.profile.user.username
   return render(request, "worker_details.html", {"work_profile": work_profile, "username": username})

    # worker_profile = get_object_or_404(WorkerProfile, pk=pk)
    # return render(request, 'worker_profile.html', {'worker_profile': worker_profile})
    # # try:
    # #     user_profile = get_object_or_404(UserProfile, pk=pk)
    # # except UserProfile.DoesNotExist:
    # #     raise Http404("Question does not exist")
    # # return render(request, "work_profile.html", {"user_profile": user_profile})


def client_profile(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    return render(request, "client_profile.html", {"user_profile": user_profile})


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