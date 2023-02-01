from django.urls import path,include
from . import views
urlpatterns = [
    path('accounts/', views.all_account,name='accounts'),
    path('account/', views.get_account,name='account'),
    path('create/', views.create_account,name='create'),
    path('create-multi/', views.create_multi,name='create-multi'),
    path('update-name/', views.update_name,name='update'),
    path('name-multi/', views.update_name_multi,name='update-multi'),
    path('deposit/', views.deposit,name='deposit'),
    path('deposit-multi/', views.deposit_multi,name='deposit-multi'),
    path('debit/', views.debit,name='debit'),
    path('debit-multi/', views.debit_multi,name='debit-multi'),
    path('delete/', views.delete_account,name='delete'),
    path('delete-multi/', views.delete_acc_multi,name='delete-multi'),
    path('delete-all/', views.del_all_account,name='delete-all'),
    path('loan/', views.get_loan,name='loan'),
    path('status/', views.status_loan,name='status'),
    path('all/', views.loan_all,name='status-all'),
    path('return/', views.return_loan,name='return'),
    path('intrest/', views.intrest,name='intrest'),
]
