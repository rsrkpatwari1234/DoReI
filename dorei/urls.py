from django.urls import path
from . import views

urlpatterns = [
    path('', views.logIn_user, name='logIn_user'),
    path('signUp/', views.signUp, name='signUp'),
    path('logInUser/', views.logIn_user, name='logIn_user'),
    path('logInSupervised/', views.logIn_manager, name='logIn_manager'),
    path('new_user/', views.new_user_signup, name='new_user_signup'),
    # path('transaction/', views.transaction, name='transaction'),
    # path('donate_money/', views.donate_money, name='donate_money'),
    # path('donate_book/', views.donate_book, name='donate_book'),
    # path('donate_stationery/', views.donate_stationery, name='donate_stationery'),
    # path('request/', views.request, name='request'),
    # path('manage/', views.manage, name='manage'),
    # path('signOut/', views.user_logIn, name='logIn_user'),
]
