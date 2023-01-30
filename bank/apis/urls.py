from django.urls import path,include
from . import views
urlpatterns = [
    path('accounts/', views.all_account,name='accounts'),
    path('account/', views.get_account,name='account'),
    path('create/', views.create_account,name='create'),
    path('update-name/', views.update_name,name='update'),
    path('deposit/', views.deposit,name='deposit'),
    path('debit/', views.debit,name='debit'),
    path('delete/', views.delete_account,name='delete'),
]