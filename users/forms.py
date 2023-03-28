from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Report, ServiceRequest,CollectionCenter,CollectionCompany, Feedback

# User Creation Form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

# Report Form
class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = '__all__'

#User Feedack Form
class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['receiver', 'text']

# Request Form

class RequestForm(ModelForm):
    class Meta:
        model = ServiceRequest
        fields = '__all__'


# New Center Form

class NewCompanyForm(ModelForm):
    class Meta:
        model = CollectionCompany
        fields = '__all__'

# New Company Form

class NewCenterForm(ModelForm):
    class Meta:
        model = CollectionCenter
        fields = '__all__'
