from django.urls import path, re_path
from . import views

# using the given urls to direct pages in the application

urlpatterns = [
    path('', views.logIn_user, name='logIn_user'),
    path('signUp/', views.signUp, name='signUp'),
    path('logInUser/', views.logIn_user, name='logIn_user'),
    path('transaction/<int:user_id>/', views.transaction, name='transaction'),
    path('donate_money/<int:user_id>/', views.donate_money, name='donate_money'),
    path('donate_book/<int:user_id>/', views.donate_book, name='donate_book'),
    path('donate_stationery/<int:user_id>/', views.donate_stationery, name='donate_stationery'),
    path('request_book/<int:user_id>/<str:isbn>/', views.request_book, name='request_book'),
    path('request_stationery/<int:user_id>/<str:stationery_id>/', views.request_stationery, name='request_stationery'),
    path('user_info/<int:user_id>/', views.user_info, name='user_info'),
    path('logInSupervised/', views.logIn_manager, name='logIn_manager'),
    #path('manage/<slug:message>/', views.manage, name='manage'),
    path('isdonated_book/<int:user_id>/<str:isbn>/', views.isdonated_book, name='isdonated_book'),
    path('isrequested_book/<int:user_id>/<str:isbn>/', views.isrequested_book, name='isrequested_book'),
    re_path(r'^manage/(?P<message>[a-zA-Z.! ]+)/$', views.manage,name='manage'),
    re_path(r'^isdonated_stationery/(?P<user_id>[0-9]+)/(?P<t_time>[-0-9_: .]+)/$', views.isdonated_stationery,name='isdonated_stationery'),
    re_path(r'^isrequested_stationery/(?P<user_id>[0-9]+)/(?P<t_time>[-0-9_:. ]+)/$', views.isrequested_stationery,name='isrequested_stationery'),
    path('locate_book/', views.locate_book, name='locate_book'),
    path('signOut/', views.signOut, name='signOut'),
]
