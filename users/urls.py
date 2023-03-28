from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.adminPage, name='dashboard'),
    path('profile/<int:pk>/', views.userPage, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('report/<int:pk>/', views.reportProblem, name='report'),
    path('request/<int:pk>/', views.requestService, name='request'),
    path('viewreports/', views.viewReports, name='viewreports'),
    path('viewrequests/', views.viewRequests, name='viewrequests'),
    path('viewcenters/<int:pk>/', views.viewCenters, name='viewcenters'),
    path('managecenters/', views.manageCenters, name='managecenters'),
    path('managecompany/', views.manageCompany, name='managecompany'),
    path('addcenter/', views.addCenter, name='addcenter'),
    path('updatecompany/<int:company_id>/', views.updateCompany, name='updatecompany'),
    path('updatecenter/<int:center_id>/', views.updateCenter, name='updatecenter'),
    path('deletecenter/<int:center_id>/', views.deleteCenter, name='deletecenter'),
    path('deletecompany/<int:company_id>/', views.deleteCompany, name='deletecompany'),
    path('deletereport/<int:report_id>/', views.deleteReport, name='deletereport'),
    path('addcompany/', views.addCompany, name='addcompany')
]