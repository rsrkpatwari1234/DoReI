from django.urls import path
from . import views

urlpatterns = [
    path('', views.logIn_user, name='logIn_user'),
    path('signUp/', views.signUp, name='signUp'),
    path('logInUser/', views.logIn_user, name='logIn_user'),
    path('logInSupervised/', views.logIn_manager, name='logIn_manager'),
    path('transaction/<int:user_id>/', views.transaction, name='transaction'),
    path('donate_money/<int:user_id>/', views.donate_money, name='donate_money'),
    path('donate_book/<int:user_id>/', views.donate_book, name='donate_book'),
    path('donate_stationery/<int:user_id>/', views.donate_stationery, name='donate_stationery'),
    path('request_book/<int:user_id>/<str:isbn>/', views.request_book, name='request_book'),
    path('request_stationery/<int:user_id>/<str:stationery_id>/', views.request_stationery, name='request_stationery'),
    path('user_info/<int:user_id>/', views.user_info, name='user_info'),
    # path('manage/', views.manage, name='manage'),
    path('signOut/', views.signOut, name='signOut'),
]
