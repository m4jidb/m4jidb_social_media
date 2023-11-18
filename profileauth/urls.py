from django.urls import path, include
from . import views


app_name = 'profileauth'

urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
    path('account-information/', views.AccountInformation.as_view(), name='account_information'),
    path('account-information/edit/', views.AccountInformationEditView.as_view(), name='account_information_edit'),
]
