from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
class SignUpForm(UserCreationForm):
    Address = forms.CharField(max_length=100, required=True)
    phone_no = forms.CharField(max_length=20, required=True)
    experiance = forms.CharField(max_length=100, required=False)
    gender = forms.ChoiceField(choices=[("male", "Male"), ("female", "Female"), ("other", "Other")], required=True)
    user_type = forms.ChoiceField(choices=[("worker", "Worker"), ("customer", "Customer")], required=True)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user_profile = UserProfile(Address=self.cleaned_data['Address'], phone_no=self.cleaned_data['phone_no'],
                                   experiance=self.cleaned_data['experiance'], gender=self.cleaned_data['gender'],
                                   user_type=self.cleaned_data['user_type'])
        if commit:
            user.save()
            user_profile.user = user
            user_profile.save()
        return user, user_profile
    
    
class worker_profile(UserCreationForm):
    service = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    price_per_day = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    available_time = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}
    # def save(self, commit=True):
    #     user = super(SignUpForm, self).save(commit=False)
    #     user_profile = UserProfile(Address=self.cleaned_data['Address'], phone_no=self.cleaned_data['phone_no'],
    #                                 gender=self.cleaned_data['gender'],
    #                                user_type=self.cleaned_data['user_type'])
    #     if commit:
    #         user.save()
    #         user_profile.user = user
    #         user_profile.save()
    #     return user, user_profile