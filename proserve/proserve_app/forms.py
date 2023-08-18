from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, WorkerProfile
class SignUpForm(UserCreationForm):
    # Address = forms.CharField(max_length=100, required=True)
    phone_no = forms.CharField(max_length=20, required=True)
    # experiance = forms.CharField(max_length=100, required=False)
    # gender = forms.ChoiceField(choices=[("male", "Male"), ("female", "Female"), ("other", "Other")], required=True)
    user_type = forms.ChoiceField(choices=[("worker", "Worker"), ("customer", "Customer")], required=True)


    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'email': 'Email'}


    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user_profile = UserProfile(Address=self.cleaned_data['Address'], phone_no=self.cleaned_data['phone_no'],
                                   
                                   user_type=self.cleaned_data['user_type'])
        if commit:
            user.save()
            user_profile.user = user
            user_profile.save()
        return user, user_profile
    

class worker_profileform(UserCreationForm):
    # class Meta:
    #     model = WorkerProfile
    #     fields = ['user','service', 'description', 'price_per_day', 'available_time', 'experiance']

    service = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    price_per_day = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    available_time = forms.CharField(max_length=100, required=False)
    experiance = forms.CharField(max_length=100, required=False)
    gender = forms.ChoiceField(choices=[("male", "Male"), ("female", "Female"), ("other", "Other")], required=True)

    # def save(self, commit=True):
    #     # user = super(SignUpForm, self).save(commit=False)
    #     user_profile = UserProfile(service=self.cleaned_data['service'], description=self.cleaned_data['description'],
    #                                experiance=self.cleaned_data['experiance'], gender=self.cleaned_data['price_per_day'],
    #                                available_time=self.cleaned_data['available_time'])
    #     if commit:
            
        
    #         user_profile.save()
    #     return  user_profile

    