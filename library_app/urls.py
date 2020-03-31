from django.urls import path
from . import views

app_name = 'library_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('createBookLoan/', views.checkout_book, name="checkout_book"),
    path('hand-inBook/', views.checkin_book, name="checkin_book"),
    path('checkout_magazine/', views.checkout_magazine, name="checkout_magazine"),
    path('checkin_magazine/', views.checkin_magazine, name="checkin_magazine"),
    path('outstanding_loans/', views.outstanding_loans, name="outstanding_loans"),
]
