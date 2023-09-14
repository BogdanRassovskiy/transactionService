from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import include#,path

urlpatterns = [
    path('transaction/', views.transaction,name="transaction"), #do transaction
    path('save_transaction/', views.save_transaction,name="save_transaction"), #save transaction
    path('ed_transactions/', views.ed_transactions,name="ed_transactions"), #edit transactions
    path('edit_transactions/', views.edit_transactions,name="edit_transactions"), #edit transactions
    

]
