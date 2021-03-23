from django.shortcuts import render

from django.http import HttpResponse
from dorei.models import *

from django.contrib import messages
from django.db import connection


def insert_using_raw_sql(sql):
    print('sql - ', sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        return True
    except:
        return False

def select_using_raw_sql(sql):
    print('sql - ', sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
    except:
        print('error in sql')
    results = cursor.fetchall()
    #print(results)
    l = []
    for  i in range(len(results)):
        dict = {}
        field = 0
        while True:
            try:
                dict[cursor.description[field][0]] = str(results[i][field])
                field = field +1
            except IndexError as e:
                break
        l.append(dict)
    return l


def logIn_user(request):
    return render(request, 'logInUser.html')

def logIn_manager(request):
    return render(request, 'logInManager.html')

def signUp(request):
    return render(request, 'SignUp.html')

def new_user_signup(request):

    if request.method == "POST":
        results = select_using_raw_sql("SELECT * FROM dorei_user")
        #print(results)
        print("Working.....")
        for user in results:
            if user['email_address'] == request.POST.get("email"):
                messages.warning(request, 'This email address has been taken!')
                return render(request, 'SignUp.html')
        
        messages.success(request, 'Your account has been created successfully!')
        return render(request, 'SignUp.html')
    else:
        return render(request, 'logInUser.html')

def signOut(request):
    return render(request, 'logInUser.html')

def transaction(request):
    return render(request, 'user_ui.html')

def donate_money(request):
    return render(request, 'donate_money.html')

def donate_book(request):
    return render(request, 'donate_book.html')

def donate_stationery(request):
    return render(request, 'donate_stationery.html')


