from urllib import request
from django.shortcuts import render, redirect
from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.core.mail import send_mail  
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


from .models import *
from .forms import CreateUserForm, ReportForm, RequestForm,FeedbackForm,NewCenterForm,NewCompanyForm
from django.contrib.auth import authenticate, login,logout
from .filters import ReportFilter, CompanyFilter
from django.contrib.auth.forms import UserCreationForm
from .decorators import unauthenticated_user, allowed_users, admin_only




from .models import *


# Create your views here.

def home(request):
    return render(request, 'users/home.html')


def contact(request):
    return render(request, 'users/contact.html')

# Register page
@unauthenticated_user
def register(request):
        form = CreateUserForm()
        
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='member')
                user.groups.add(group)
                
                messages.success(request, 'Account Created Successfully ' + ' ' + username + ' '+  'Please Wait For Verification')
                return redirect('login')


        context = {'form': form}
        return render(request, 'users/register.html', context)


# User login page
@unauthenticated_user
def loginPage(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR Password Is Incorrect')
                context = {}
                return render(request, 'users/login.html', context)
                

        context = {}
        return render(request, 'users/login.html', context)

# Logout Function

def logoutUser(request):
    logout(request)
    return redirect('home')


# User home page
@login_required(login_url='login')
@allowed_users(allowed_roles=['member'])
def userPage(request,pk):
    companies = CollectionCompany.objects.all()
    total_companies = companies.count()

    centers = CollectionCenter.objects.all()
    total_centers = centers.count()

    member = Member.objects.get(id=pk)

    feedbacks = member.feedbacks.all()
    feedback_count = feedbacks.count()

    context = {'feedback_count':feedback_count, 'companies':companies, 'total_companies':total_companies, 'centers':centers,'total_centers':total_centers, 'feedbacks':feedbacks,'pk':pk  }
    return render(request, 'users/userpage.html', context)

# Report page view
@login_required(login_url='login')
def reportProblem(request, pk):
        form = ReportForm()
        member = Member.objects.get(id=pk)
        
        if request.method == 'POST':
            form = ReportForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Report Sent Successfully')
                profile_url = reverse('profile', args=[pk])
                return redirect(profile_url)


        context = {'form': form, 'member':member, 'pk':pk}
        return render(request, 'users/report.html', context)


# Administrator page view function
@login_required(login_url='login')
@admin_only
def adminPage(request):
    companies = CollectionCompany.objects.all()
    total_companies = companies.count()

    centers = CollectionCenter.objects.all()
    total_centers = centers.count()

    reports = Report.objects.all()
    total_reports = reports.count()

    requests = ServiceRequest.objects.all()
    total_requests = requests.count()

    # Sending User Feedack
    form = FeedbackForm()
        
    if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Feedback Successfully Sent')
                return redirect('dashboard')




    context = {'form':form, 'total_companies':total_companies, 'total_centers':total_centers, 'total_reports':total_reports, 'total_requests':total_requests}
    return render(request, 'users/dashboard.html', context)
#Request Function View

@login_required(login_url='login')
@allowed_users(allowed_roles=['member'])
def requestService(request, pk):
        
        form = RequestForm()
        
        if request.method == 'POST':
            form = RequestForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Request Sent Successfully')
                profile_url = reverse('profile', args=[pk])
                return redirect(profile_url)


        context = {'form': form, 'pk':pk}
        return render(request, 'users/request.html', context)



# View Centers Function
@login_required(login_url='login')
@allowed_users(allowed_roles=['member'])
def viewCenters(request, pk):
    collection_centers = CollectionCenter.objects.all()

    context = {'collection_centers': collection_centers, 'pk':pk}
    return render(request, 'users/viewcenters.html', context)

#View Reports Function
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewReports(request):
    reports = Report.objects.all()

    companies = CollectionCompany.objects.all()
    total_companies = companies.count()

    centers = CollectionCenter.objects.all()
    total_centers = centers.count()

    reports = Report.objects.all()
    total_reports = reports.count()

    requests = ServiceRequest.objects.all()
    total_requests = requests.count()

    #filter search
    myFilter = ReportFilter(request.GET, queryset=reports)
    reports = myFilter.qs

    context = {'total_companies':total_companies, 'total_centers':total_centers, 'total_reports':total_reports, 'total_requests':total_requests, 'reports':reports, 'myFilter':myFilter}
    return render(request, 'users/viewreports.html', context)

# Delete Reports
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteReport(request, report_id):
    report = Report.objects.get(pk=report_id)
    if request.method == "POST":
        report.delete()
        return redirect('viewreports')

    context = {'report':report, 'report_id':report_id}
    return render(request, 'users/deletereport.html', context)

# Delete Requests
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteRequest(request, request_id):
    requestmade = ServiceRequest.objects.get(pk=request_id)
    if request.method == "POST":
        requestmade.delete()
        return redirect('viewrequests')

    context = {'requestmade':requestmade, 'request_id':request_id}
    return render(request, 'users/deleterequest.html', context)

#Collection Centers
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def manageCenters(request):
    collection_centers = CollectionCenter.objects.all()

    companies = CollectionCompany.objects.all()
    total_companies = companies.count()

    centers = CollectionCenter.objects.all()
    total_centers = centers.count()

    reports = Report.objects.all()
    total_reports = reports.count()

    requests = ServiceRequest.objects.all()
    total_requests = requests.count()

    context = {'collection_centers':collection_centers, 'total_companies':total_companies, 'total_centers':total_centers, 'total_reports':total_reports, 'total_requests':total_requests, 'reports':reports}
    return render(request, 'users/disposalcenters.html', context)


# Add Center Form
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addCenter(request):
        
        form = NewCenterForm()
        
        if request.method == 'POST':
            form = NewCenterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Center Added Successfully')
                return redirect('dashboard')


        context = {'form': form}
        return render(request, 'users/addcenter.html', context)

# Update Company Information
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCenter(request, center_id):
    center = CollectionCenter.objects.get(pk=center_id)
    if request.method == "POST":
        form = NewCenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            return redirect('managecenters')
    else:
        form = NewCenterForm(instance=center)
    return render(request, 'users/editcenter.html', {'form': form, 'center':center})

# Delete Center
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCenter(request, center_id):
    center = CollectionCenter.objects.get(pk=center_id)
    if request.method == "POST":
        center.delete()
        return redirect('managecenters')

    context = {'item':center, 'center_id':center_id}
    return render(request, 'users/deletecenter.html', context)



# Collection Companies
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def manageCompany(request):
    collection_companies = CollectionCompany.objects.all()
    total_companies = collection_companies.count()

    centers = CollectionCenter.objects.all()
    total_centers = centers.count()

    reports = Report.objects.all()
    total_reports = reports.count()

    requests = ServiceRequest.objects.all()
    total_requests = requests.count()

    #filter search
    compFilter = CompanyFilter(request.GET, queryset=collection_companies)
    collection_companies = compFilter.qs

    context = {'collection_companies':collection_companies, 'total_companies':total_companies, 'total_centers':total_centers, 'total_reports':total_reports, 'total_requests':total_requests, 'reports':reports, 'compFilter':compFilter}
    return render(request, 'users/companies.html', context)

# Update Company Information
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCompany(request, company_id):
    company = CollectionCompany.objects.get(pk=company_id)
    if request.method == "POST":
        form = NewCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('managecompany')
    else:
        form = NewCompanyForm(instance=company)
    return render(request, 'users/editcompany.html', {'form': form, 'company':company})

# Add Company Form
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addCompany(request):
        form = NewCompanyForm()
        
        if request.method == 'POST':
            form = NewCompanyForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Company Added Successfully')
                return redirect('dashboard')

        context = {'form': form}
        return render(request, 'users/addcompany.html', context)


# Delete Company
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCompany(request, company_id):
    company = CollectionCompany.objects.get(pk=company_id)
    if request.method == "POST":
        company.delete()
        return redirect('managecompany')

    context = {'company':company, 'company_id':company_id}
    return render(request, 'users/deletecompany.html', context)


# View Requests
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewRequests(request):
    requests = ServiceRequest.objects.all()

    companies = CollectionCompany.objects.all()
    total_companies = companies.count()

    centers = CollectionCenter.objects.all()
    total_centers = centers.count()

    reports = Report.objects.all()
    total_reports = reports.count()

    requests = ServiceRequest.objects.all()
    total_requests = requests.count()

    #filter search
    myFilter = ReportFilter(request.GET, queryset=reports)
    reports = myFilter.qs

    context = {'total_companies':total_companies, 'total_centers':total_centers, 'total_reports':total_reports, 'total_requests':total_requests, 'requests':requests, 'myFilter':myFilter}
    return render(request, 'users/viewrequests.html', context)