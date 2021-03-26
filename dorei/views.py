from django.shortcuts import render, redirect

from django.http import HttpResponse
from dorei.models import *

from django.contrib import messages
from django.db import connection

from datetime import datetime

from django.urls import reverse

import json

def insert_using_raw_sql(sql):
    print('sql - ', sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        return True
    except Exception as e:
        print(e)
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

    if request.method == "POST":
        email = request.POST.get("email")
        results = select_using_raw_sql("SELECT du.user_id,du.password FROM dorei_user AS du WHERE du.email_address='" + str(email) + "'")
        
        if results:
            for user in results:
                if user['password'] == request.POST.get("password"):
                    #return render(request, 'user_ui.html', {'current_user':user['user_id']})
                    return redirect(reverse('transaction', kwargs={"user_id": user['user_id']}))
        else:
            messages.error(request, 'Email id or password does not match!')
            
    return render(request, 'logInUser.html')

def logIn_manager(request):
    return render(request, 'logInManager.html')

def signUp(request):

    if request.method == "POST":
        results = select_using_raw_sql("SELECT * FROM dorei_user")
        #print(results)
        print("Working.....")
        count = 0
        for user in results:
            if user['email_address'] == request.POST.get("email"):
                messages.error(request, 'This email address has been taken!')
                return render(request, 'SignUp.html') 

            count = count + 1

        if request.POST.get("password") != request.POST.get("repeat_password"):
            messages.error(request, 'Password does not match!')
            return render(request, 'SignUp.html')


        UserId = count+1
        FirstName = request.POST.get("first_name")
        MiddleName = request.POST.get("middle_name")
        LastName = request.POST.get("last_name")
        Email = request.POST.get("email")
        HouseNo = request.POST.get("house_no")
        StreetNo = request.POST.get("street_no")
        StreetName = request.POST.get("street_name")
        City = request.POST.get("city")
        State = request.POST.get("state")
        PostalCode = request.POST.get("zipcode")
        Password = request.POST.get("password")

        if len(HouseNo) == 0:
            HouseNo = 'NULL'
        if len(StreetNo) == 0:
            StreetNo = 'NULL'
        if len(MiddleName) == 0:
            MiddleName = 'NULL'
        if len(LastName) == 0:
            LastName = 'NULL'

        #print(type(UserId),type(FirstName),type(Email),type(HouseNo),type(StreetName),type(City),type(PostalCode),type(Password))

        i = "dorei_user(user_id,postal_code,first_name,middle_name,last_name,email_address,house_number,street_number,street_name,city,state,password)"
        j = "values("+str(UserId)+","+str(PostalCode)+",'"+str(FirstName)+"',"+str(MiddleName)+","+str(LastName)+",'"+str(Email)+"',"+str(HouseNo)+","+str(StreetNo)+",'"+str(StreetName)+"','"+str(City)+"','"+str(State)+"','"+str(Password)+"')"
        

        command = "INSERT INTO " + i +" "+ j
        if insert_using_raw_sql(command):
            # insert phone number
            messages.success(request, 'Your account has been created successfully!')
            # return render(request, 'logInUser.html')
            return redirect('/dorei/logInUser/')
        else:
            messages.error(request, 'Internal error! Try again.')
            #return render(request, 'SignUp.html')  
            return redirect('/dorei/signUp/')

        # user = User.objects.create(user_id=UserId, email_address=Email, first_name=FirstName, middle_name=MiddleName,
        #                            last_name=LastName, house_number=HouseNo, street_number=StreetNo, street_name=StreetName, 
        #                            city=City, state=State, postal_code=PostalCode, password=Password)
        # messages.success(request, 'Your account has been created successfully!')
        # return render(request, 'logInUser.html')

    else:
        return render(request, 'SignUp.html')

def signOut(request):
    return redirect('/dorei/logInUser/')

def transaction(request, user_id):
    return render(request, 'user_ui.html', {'id':user_id})

def donate_money(request, user_id):

    if request.method == "POST":
        MoneyId = Money.objects.all().count() + 1
        UserId = user_id
        Time =  datetime.now()
        TransactionId = request.POST.get("t_id")
        Amount = request.POST.get("amount") 

        i = "dorei_money(money_id,user_id,t_time,amount,transaction_id)"
        j = "values("+str(MoneyId)+","+str(UserId)+",'"+str(Time)+"',"+str(Amount)+",'"+str(TransactionId)+"')"
        
        command = "INSERT INTO " + i +" "+ j
        if insert_using_raw_sql(command):
            results = select_using_raw_sql("SELECT * FROM dorei_money")
            print(json.dumps(results,indent=4))
            messages.success(request, 'Thank you for donating money.')
            return redirect(reverse('transaction', kwargs={"user_id":user_id}))
        else:
            messages.error(request, 'Internal error! Try again.')
        
    return render(request, 'donate_money.html', {'user_id':user_id})

def donate_book(request, user_id):

    if request.method == "POST":
        Isbn = Book.objects.all().count() + 1
        Author = request.POST.get("author")
        Subject = request.POST.get("subject")
        Title = request.POST.get("title")
        Edition = request.POST.get("edition")
        Grade = request.POST.get("class")

        i = "dorei_book(isbn, author, subject, title, edition, grade)"
        j = "values('"+str(Isbn)+"','"+str(Author)+"','"+str(Subject)+"','"+str(Title)+"',"+str(Edition)+","+str(Grade)+")"
        
        command1 = "INSERT INTO " + i +" "+ j

        UserId = user_id
        Time =  datetime.now()

        i = "dorei_bookdonate(user_id, isbn, t_time, is_collected)"
        j = "values("+str(UserId)+",'"+str(Isbn)+"','"+str(Time)+"','False')"
        
        command2 = "INSERT INTO " + i +" "+ j

        if insert_using_raw_sql(command1) and insert_using_raw_sql(command2):
            results = select_using_raw_sql("SELECT * FROM dorei_book")
            print(json.dumps(results,indent=4))

            results = select_using_raw_sql("SELECT * FROM dorei_bookdonate")
            print(json.dumps(results,indent=4))

            messages.success(request, 'Thank you for donating Book(s).')
            return redirect(reverse('transaction', kwargs={"user_id":user_id}))
        else:
            messages.error(request, 'Internal error! Try again.')
    return render(request, 'donate_book.html', {'user_id':user_id})

def donate_stationery(request, user_id):
    if request.method == "POST":
        StationeryId = Stationery.objects.all().count() + 1
        StationeryName = request.POST.get("stationery_name")
        Quantity = request.POST.get("tot_quantity")

        i = "dorei_stationery(stationery_id, stationery_name, tot_quantity)"
        j = "values("+str(StationeryId)+",'"+str(StationeryName)+"',"+str(Quantity)+")"
        
        command1 = "INSERT INTO " + i +" "+ j

        UserId = user_id
        Time =  datetime.now()

        i = "dorei_stationerydonate(user_id, stationery_id, t_time, quantity, is_collected)"
        j = "values("+str(UserId)+","+str(StationeryId)+",'"+str(Time)+"',"+str(Quantity)+",'False')"
        
        command2 = "INSERT INTO " + i +" "+ j

        if insert_using_raw_sql(command1) and insert_using_raw_sql(command2):
            results = select_using_raw_sql("SELECT * FROM dorei_stationery")
            print(json.dumps(results,indent=4))

            results = select_using_raw_sql("SELECT * FROM dorei_stationerydonate")
            print(json.dumps(results,indent=4))

            messages.success(request, 'Thank you for donating Item(s).')
            return redirect(reverse('transaction', kwargs={"user_id":user_id}))
        else:
            messages.error(request, 'Internal error! Try again.')
    return render(request, 'donate_stationery.html', {'user_id':user_id})

def request(request):
    return render(request, 'request.html')
