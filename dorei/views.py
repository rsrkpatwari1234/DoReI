from django.shortcuts import render, redirect

from django.http import HttpResponse
from dorei.models import *

from django.contrib import messages
from django.db import connection

from datetime import datetime

from django.urls import reverse

import json

# inserting using raw sql of django
def insert_using_raw_sql(sql):
    print('sql - ', sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        return True
    except Exception as e:
        print(e)
        return False

# updating using raw sql of django
def update_using_raw_sql(sql):
    print('sql - ', sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        return True
    except Exception as e:
        print(e)
        return False

# select using raw sql of django
def select_using_raw_sql(sql):
    print('sql - ', sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
        return []
    results = cursor.fetchall()
    ##print(results)
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

# alredy signed up user log in into the system
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

# new user tries to sign up
def signUp(request):

    if request.method == "POST":
        results = select_using_raw_sql("SELECT * FROM dorei_user")
        for user in results:
            if user['email_address'] == request.POST.get("email"):
                messages.error(request, 'This email address has been taken!')
                return render(request, 'SignUp.html') 

        if request.POST.get("password") != request.POST.get("repeat_password"):
            messages.error(request, 'Password does not match!')
            return render(request, 'SignUp.html')


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

        i = "dorei_user(postal_code,first_name,middle_name,last_name,email_address,house_number,street_number,street_name,city,state,password)"
        j = "values("+str(PostalCode)+",'"+str(FirstName)+"','"+str(MiddleName)+"','"+str(LastName)+"','"+str(Email)+"','"+str(HouseNo)+"','"+str(StreetNo)+"','"+str(StreetName)+"','"+str(City)+"','"+str(State)+"','"+str(Password)+"')"
        

        command = "INSERT INTO " + i +" "+ j
        if insert_using_raw_sql(command):
            result = select_using_raw_sql("SELECT du.user_id FROM dorei_user AS du WHERE du.email_address='"+str(Email)+"'")
            print(json.dumps(results,indent=4))
            result = insert_using_raw_sql("INSERT INTO dorei_phonenumber(user_id, phone_number) VALUES("+str(result[0]['user_id'])+","+str(request.POST.get("phone_no"))+")")
            print(json.dumps(results,indent=4))
            messages.success(request, 'Your account has been created successfully!')
            return redirect('/dorei/logInUser/')
        else:
            messages.error(request, 'Internal error! Try again.') 
            return redirect('/dorei/signUp/')

        # user = User.objects.create(user_id=UserId, email_address=Email, first_name=FirstName, middle_name=MiddleName,
        #                            last_name=LastName, house_number=HouseNo, street_number=StreetNo, street_name=StreetName, 
        #                            city=City, state=State, postal_code=PostalCode, password=Password)
        # messages.success(request, 'Your account has been created successfully!')
        # return render(request, 'logInUser.html')

    else:
        return render(request, 'SignUp.html')

# user or manager tries to sign out of the application
def signOut(request):
    return redirect('/dorei/logInUser/')

# transaction details and features available to the user of the application
def transaction(request, user_id):

    total_charity = select_using_raw_sql("SELECT SUM(dm.amount) FROM dorei_money AS dm")
    
    books_donated = select_using_raw_sql("SELECT COUNT(db.isbn) FROM dorei_bookdonate AS db WHERE db.is_collected=1")
    stationery_donated = select_using_raw_sql("SELECT SUM(ds.quantity) FROM dorei_stationerydonate AS ds WHERE ds.is_collected=1")
    
    book_donors = select_using_raw_sql("SELECT COUNT(DISTINCT(db.user_id)) FROM dorei_bookdonate AS db WHERE db.is_collected=1")
    stationery_donors = select_using_raw_sql("SELECT COUNT(DISTINCT(ds.user_id)) FROM dorei_stationerydonate AS ds WHERE ds.is_collected=1")
    
    recent_book_donation = select_using_raw_sql("SELECT UPPER(du.first_name) AS name,UPPER(db.title) AS title,dbd.t_time AS t_time\
     FROM dorei_bookdonate AS dbd, dorei_book AS db, dorei_user AS du\
     WHERE dbd.is_collected=1 AND du.user_id=dbd.user_id AND db.isbn=dbd.isbn ORDER BY dbd.t_time DESC LIMIT 5")
    recent_stationery_donation = select_using_raw_sql("SELECT UPPER(du.first_name) AS name,UPPER(ds.stationery_name) AS category,dsd.quantity AS quantity,dsd.t_time AS t_time\
     FROM dorei_stationerydonate AS dsd, dorei_stationery AS ds, dorei_user AS du\
     WHERE dsd.is_collected=1 AND du.user_id=dsd.user_id AND ds.stationery_id=dsd.stationery_id ORDER BY dsd.t_time DESC LIMIT 5")

    books_available = []
    subject = 'Select a Subject'
    stationery_available = []
    category = 'Select a Category'

    if request.method == "POST":
        subject = request.POST.get("subject")
        if subject != 'Select a Subject':
            books_available = select_using_raw_sql("SELECT db.isbn as isbn, UPPER(db.title) as title,UPPER(db.author) as author,db.grade as grade,db.edition as edition \
            FROM dorei_bookdonate AS dbd,dorei_book as db\
            WHERE  db.isbn=dbd.isbn AND dbd.is_collected=1 AND db.subject='"+str(subject)+"' AND \
            dbd.isbn NOT IN(SELECT dbr.isbn FROM dorei_bookrequest AS dbr)") 

        category = request.POST.get("category")
        print(category)
        if category != 'Select a Category':
            stationery_available = select_using_raw_sql("SELECT ds.stationery_id as stationery_id,ds.stationery_name as name,ds.tot_quantity as quantity \
            FROM dorei_stationery AS ds\
            WHERE  ds.stationery_name='"+str(category)+"' AND ds.tot_quantity>0") 
            results = select_using_raw_sql("SELECT * FROM dorei_stationery")

    data = {
            'id':user_id,
            'charity':total_charity[0]['SUM(dm.amount)'],
            'books_donated':books_donated[0]['COUNT(db.isbn)'],
            'stationery_donated':stationery_donated[0]['SUM(ds.quantity)'],
            'book_donors':book_donors[0]['COUNT(DISTINCT(db.user_id))'],
            'stationery_donors':stationery_donors[0]['COUNT(DISTINCT(ds.user_id))'],
            'recent_book_donation':recent_book_donation,
            'recent_stationery_donation':recent_stationery_donation,
            'books_available':books_available,
            'subject':subject,
            'stationery_available':stationery_available,
            'category':category,
        }
    return render(request, 'user_ui.html', data)

# a logged in user donates money for the organisation
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
            #print(json.dumps(results,indent=4))
            messages.success(request, 'Thank you for donating money.')
            return redirect(reverse('transaction', kwargs={"user_id":user_id}))
        else:
            messages.error(request, 'Internal error! Try again.')
        
    return render(request, 'donate_money.html', {'user_id':user_id})

# a logged in user donates a book for the organisation
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
            #print(json.dumps(results,indent=4))

            results = select_using_raw_sql("SELECT * FROM dorei_bookdonate")
            #print(json.dumps(results,indent=4))

            messages.success(request, 'Thank you for donating Book(s).')
            return redirect(reverse('transaction', kwargs={"user_id":user_id}))
        else:
            messages.error(request, 'Internal error! Try again.')
    return render(request, 'donate_book.html', {'user_id':user_id})

# a logged in user donates a stationery for the organisation
def donate_stationery(request, user_id):
    if request.method == "POST":

        StationeryName = request.POST.get("stationery_name")
        Quantity = request.POST.get("tot_quantity")

        results = select_using_raw_sql("SELECT ds.stationery_id FROM dorei_stationery AS ds WHERE ds.stationery_name='"+str(StationeryName)+"'")
        
        if len(results) == 0:
            command = "INSERT INTO dorei_stationery(stationery_name,tot_quantity) VALUES('"+str(StationeryName)+"',0)"
            insert_using_raw_sql(command)
            results = select_using_raw_sql("SELECT ds.stationery_id FROM dorei_stationery AS ds WHERE ds.stationery_name='"+str(StationeryName)+"'")     
        
        #print(json.dumps(results,indent=4))
        StationeryId = results[0]['stationery_id']

        UserId = user_id
        Time =  datetime.now()

        i = "dorei_stationerydonate(user_id, stationery_id, t_time, quantity, is_collected)"
        j = "values("+str(UserId)+","+str(StationeryId)+",'"+str(Time)+"',"+str(Quantity)+",'False')"
        
        command = "INSERT INTO " + i +" "+ j

        if insert_using_raw_sql(command):
            results = select_using_raw_sql("SELECT * FROM dorei_stationerydonate")
            #print(json.dumps(results,indent=4))

            messages.success(request, 'Thank you for donating Item(s).')
            return redirect(reverse('transaction', kwargs={"user_id":user_id}))
        else:
            messages.error(request, 'Internal error! Try again.')
    return render(request, 'donate_stationery.html', {'user_id':user_id})

#  logged in user requests for a particular book
def request_book(request, user_id, isbn):

    Time =  datetime.now()
    command = "INSERT INTO dorei_bookrequest(isbn, user_id, t_time, is_delivered) \
    values('"+str(isbn)+"',"+str(user_id)+",'"+str(Time)+"','False')"

    if insert_using_raw_sql(command):
        results = select_using_raw_sql("SELECT * FROM dorei_bookrequest")
        #print(json.dumps(results,indent=4))
        messages.success(request, 'Thank you for the Book request.')
    else:
        messages.error(request, 'Internal error! Try again.')
    return redirect(reverse('transaction', kwargs={"user_id":user_id}))

# logged in user requests for a particular stationery
def request_stationery(request, user_id, stationery_id):

    Time =  datetime.now()
    command1 = "INSERT INTO dorei_stationeryrequest(stationery_id, user_id, t_time, quantity, is_delivered) \
    values("+str(stationery_id)+","+str(user_id)+",'"+str(Time)+"',1,'False')"

    command2 = "UPDATE dorei_stationery SET tot_quantity=tot_quantity-1 WHERE stationery_id="+str(stationery_id)

    if insert_using_raw_sql(command1) and update_using_raw_sql(command2):
        results = select_using_raw_sql("SELECT * FROM dorei_stationery")
        #print(json.dumps(results,indent=4))

        results = select_using_raw_sql("SELECT * FROM dorei_stationeryrequest")
        #print(json.dumps(results,indent=4))
        messages.success(request, 'Thank you for the Stationery request.')
    else:
        messages.error(request, 'Internal error! Try again.')
    return redirect(reverse('transaction', kwargs={"user_id":user_id}))

# transaction and phone number details of a particular user
def user_info(request, user_id):

    m_donations = select_using_raw_sql("SELECT dm.amount as amount,date(dm.t_time) as t_time FROM dorei_money AS dm WHERE dm.user_id="+str(user_id))
    
    br_donations = select_using_raw_sql("SELECT UPPER(db.title) as title,db.subject as subject,db.author as author,date(dbd.t_time) as t_time FROM dorei_bookdonate AS dbd,dorei_book as db\
     WHERE dbd.user_id="+str(user_id)+" AND db.isbn=dbd.isbn AND dbd.is_collected=1")
    bnr_donations = select_using_raw_sql("SELECT UPPER(db.title) as title,db.subject as subject,db.author as author,date(dbd.t_time) as t_time FROM dorei_bookdonate AS dbd,dorei_book as db\
     WHERE dbd.user_id="+str(user_id)+" AND db.isbn=dbd.isbn AND dbd.is_collected<>1")

    sr_donations = select_using_raw_sql("SELECT ds.stationery_name as name,dsd.quantity as quantity,date(dsd.t_time) as t_time FROM dorei_stationerydonate AS dsd,dorei_stationery as ds\
     WHERE dsd.user_id="+str(user_id)+" AND ds.stationery_id=dsd.stationery_id AND dsd.is_collected=1")
    snr_donations = select_using_raw_sql("SELECT ds.stationery_name as name,dsd.quantity as quantity,date(dsd.t_time) as t_time FROM dorei_stationerydonate AS dsd,dorei_stationery as ds\
     WHERE dsd.user_id="+str(user_id)+" AND ds.stationery_id=dsd.stationery_id AND dsd.is_collected<>1")

    b_requests = select_using_raw_sql("SELECT UPPER(db.title) as title,db.subject as subject,db.author as author,date(dbr.t_time) as t_time FROM dorei_bookrequest AS dbr,dorei_book as db\
     WHERE dbr.user_id="+str(user_id)+" AND db.isbn=dbr.isbn AND dbr.is_delivered=1")
    bp_requests = select_using_raw_sql("SELECT UPPER(db.title) as title,db.subject as subject,db.author as author,date(dbr.t_time) as t_time FROM dorei_bookrequest AS dbr,dorei_book as db\
     WHERE dbr.user_id="+str(user_id)+" AND db.isbn=dbr.isbn AND dbr.is_delivered<>1")
    print(json.dumps(bp_requests,indent=4))
    result = select_using_raw_sql("SELECT * FROM dorei_bookrequest")
    print(json.dumps(result,indent=4))
    s_requests = select_using_raw_sql("SELECT ds.stationery_name as name,dsr.quantity as quantity,date(dsr.t_time) as t_time FROM dorei_stationeryrequest AS dsr,dorei_stationery as ds\
     WHERE dsr.user_id="+str(user_id)+" AND ds.stationery_id=dsr.stationery_id AND dsr.is_delivered=1")
    sp_requests = select_using_raw_sql("SELECT ds.stationery_name as name,dsr.quantity as quantity,date(dsr.t_time) as t_time FROM dorei_stationeryrequest AS dsr,dorei_stationery as ds\
     WHERE dsr.user_id="+str(user_id)+" AND ds.stationery_id=dsr.stationery_id AND dsr.is_delivered<>1")

    phone_number = select_using_raw_sql("SELECT p.phone_number AS phone_number FROM dorei_phonenumber AS p\
     WHERE p.user_id="+str(user_id))

    if request.method == "POST":
        
        command = "INSERT INTO dorei_phonenumber(user_id,phone_number) values("+str(user_id)+","+str(request.POST.get("phone_number"))+")"
        if insert_using_raw_sql(command):
            phone_number = select_using_raw_sql("SELECT p.phone_number AS phone_number FROM dorei_phonenumber AS p\
                WHERE p.user_id="+str(user_id))
            messages.success(request, 'Phone number stored.')
        else:
            messages.error(request, 'Internal error! Try again.')

    data = {
            'id':user_id,
            'm_donations':m_donations,
            'br_donations':br_donations,
            'bnr_donations':bnr_donations,
            'sr_donations':sr_donations,
            'snr_donations':snr_donations,
            'b_requests':b_requests,
            'bp_requests':bp_requests,
            's_requests':s_requests,
            'sp_requests':sp_requests,
            'phone_number':phone_number,
        }

    return render(request, 'user_info.html', data)

# log in facility for the manager of the application
def logIn_manager(request):
    if request.method == "POST":
        email = request.POST.get("email")
        results = select_using_raw_sql("SELECT dm.manager_id,dm.password FROM dorei_manager AS dm WHERE dm.email_address='" + str(email) + "'")
        
        if results:
            for user in results:
                if user['password'] == request.POST.get("password"):
                    return redirect(reverse('manage'))
        else:
            messages.error(request, 'Email id or password does not match!')
            
    return render(request, 'logInManager.html')

# Overall transactions and facilities available to the manager
def manage(request):

    total_charity = select_using_raw_sql("SELECT SUM(dm.amount) FROM dorei_money AS dm")

    books_donated = select_using_raw_sql("SELECT COUNT(db.isbn) FROM dorei_bookdonate AS db WHERE db.is_collected=1")
    stationery_donated = select_using_raw_sql("SELECT SUM(ds.quantity) FROM dorei_stationerydonate AS ds WHERE ds.is_collected=1")

    book_donors = select_using_raw_sql("SELECT COUNT(DISTINCT(db.user_id)) FROM dorei_bookdonate AS db WHERE db.is_collected=1")
    stationery_donors = select_using_raw_sql("SELECT COUNT(DISTINCT(ds.user_id)) FROM dorei_stationerydonate AS ds WHERE ds.is_collected=1")

    charity_details = select_using_raw_sql("SELECT date(dm.t_time) AS t_time,dm.user_id AS user_id,dm.amount AS amount FROM dorei_money AS dm")
    user_details = select_using_raw_sql("SELECT du.user_id AS user_id,du.first_name||' '||du.middle_name||' '||du.last_name AS name,du.email_address AS  email,\
        du.house_number AS house_number,du.street_number AS street_number,du.street_name AS street_name,du.city AS city,du.state AS state,du.postal_code AS postal_code\
        FROM dorei_user AS du")

    book_location = select_using_raw_sql("SELECT db.isbn AS isbn,UPPER(db.title) AS title,dl.floor AS floor,dl.room AS room,dl.shelf AS shelf \
     FROM dorei_book AS db, dorei_location AS dl WHERE db.location_id IS NOT NULL AND dl.location_id=db.location_id")

    book_donations = select_using_raw_sql("SELECT dbd.user_id AS user_id,date(dbd.t_time) AS t_time,dbd.isbn AS isbn,db.title AS title,db.subject AS subject,dbd.is_collected AS verify\
     FROM dorei_bookdonate AS dbd, dorei_book AS db WHERE db.isbn=dbd.isbn")

    book_requests = select_using_raw_sql("SELECT dbr.user_id AS user_id,date(dbr.t_time) AS t_time,dbr.isbn AS isbn,db.title AS title,db.subject AS subject,dbr.is_delivered AS verify\
     FROM dorei_bookrequest AS dbr, dorei_book AS db WHERE db.isbn=dbr.isbn")
    #print(json.dumps(book_donations,indent=4))

    available_stationery = select_using_raw_sql("SELECT ds.stationery_name AS name,ds.tot_quantity AS tot_quantity FROM dorei_stationery AS ds")
    #print(json.dumps(stationery_donations,indent=4))

    stationery_donations = select_using_raw_sql("SELECT dsd.user_id AS user_id,dsd.t_time AS t_time,ds.stationery_name AS name,dsd.quantity AS quantity,dsd.is_collected AS verify\
     FROM dorei_stationerydonate AS dsd, dorei_stationery AS ds WHERE ds.stationery_id=dsd.stationery_id")
    #print(json.dumps(stationery_donations,indent=4))

    stationery_requests = select_using_raw_sql("SELECT dsr.user_id AS user_id,dsr.t_time AS t_time,ds.stationery_name AS name,dsr.quantity AS quantity,dsr.is_delivered AS verify\
     FROM dorei_stationeryrequest AS dsr, dorei_stationery AS ds WHERE ds.stationery_id=dsr.stationery_id")
    #print(json.dumps(stationery_requests,indent=4))

    data = {
            'total_charity':total_charity[0]['SUM(dm.amount)'],
            'books_donated':books_donated[0]['COUNT(db.isbn)'],
            'stationery_donated':stationery_donated[0]['SUM(ds.quantity)'],
            'book_donors':book_donors[0]['COUNT(DISTINCT(db.user_id))'],
            'stationery_donors':stationery_donors[0]['COUNT(DISTINCT(ds.user_id))'],
            'charity_details':charity_details,
            'user_details':user_details,
            'book_location':book_location,
            'book_donations':book_donations,
            'book_requests':book_requests,
            'available_stationery':available_stationery,
            'stationery_donations':stationery_donations,
            'stationery_requests':stationery_requests,
        }

    return render(request, 'manager_ui.html', data)

# manager can verify the donation of a book and can set its location
def isdonated_book(request,user_id,isbn):
    command = "UPDATE dorei_bookdonate SET is_collected=1 WHERE user_id="+str(user_id)+" AND isbn='"+str(isbn)+"'"
    update_using_raw_sql(command)
    # results = select_using_raw_sql("SELECT * FROM dorei_bookdonate")
    # print(json.dumps(results,indent=4))
    data = {
        'isbn':isbn,
    }
    return render(request, 'locate_book.html', data)

# manager can verify the request for a book by any user
def isrequested_book(request,user_id,isbn):
    command = "UPDATE dorei_bookrequest SET is_delivered=1 WHERE user_id="+str(user_id)+" AND isbn='"+str(isbn)+"'"
    update_using_raw_sql(command)
    return redirect(reverse('manage'))

# manager can verify the donation of a stationery by any user
def isdonated_stationery(request,user_id,t_time):
    command = "UPDATE dorei_stationerydonate SET is_collected=1 WHERE user_id="+str(user_id)+" AND t_time='"+str(t_time)+"'"
    update_using_raw_sql(command)

    result = select_using_raw_sql("SELECT dsd.stationery_id as id,dsd.quantity as qty\
     FROM dorei_stationerydonate AS dsd WHERE user_id="+str(user_id)+" AND t_time='"+str(t_time)+"'")

    command = "UPDATE dorei_stationery SET tot_quantity=tot_quantity+"+str(result[0]['qty'])+" WHERE stationery_id="+str(result[0]['id'])
    update_using_raw_sql(command)

    results = select_using_raw_sql("SELECT * FROM dorei_stationery")
    print(json.dumps(results,indent=4))

    return redirect(reverse('manage'))

# manager can verify the request for a stationery by any user
def isrequested_stationery(request,user_id,t_time):
    command = "UPDATE dorei_stationeryrequest SET is_delivered=1 WHERE user_id="+str(user_id)+" AND t_time='"+str(t_time)+"'"
    #print(user_id,isbn)
    #print(command)
    update_using_raw_sql(command)
    return redirect(reverse('manage'))

# manager sets the location for a book
def locate_book(request):

    if request.method == "POST":
        isbn = request.POST.get("isbn")
        floor = request.POST.get("floor")
        room = request.POST.get("room")
        shelf = request.POST.get("shelf")

        result = select_using_raw_sql("SELECT * FROM dorei_location AS dl WHERE dl.floor="+str(floor)+" AND dl.room="+str(room)+" AND dl.shelf="+str(shelf))

        if len(result) == 0:
            command = "INSERT INTO dorei_location(floor,room,shelf) VALUES("+str(floor)+","+str(room)+","+str(shelf)+")"
            if insert_using_raw_sql(command):
                result = select_using_raw_sql("SELECT location_id FROM dorei_location AS dl WHERE dl.floor="+str(floor)+" AND dl.room="+str(room)+" AND dl.shelf="+str(shelf))
                update_using_raw_sql("UPDATE dorei_book SET location_id="+str(result[0]['location_id'])+" WHERE isbn='"+str(isbn)+"'")
        else:
            return render(request, 'locate_book.html', {'isbn':isbn})
    return redirect(reverse('manage'))