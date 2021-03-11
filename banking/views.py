from django import http
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection


# Create your views here.
def welcome(request):
    return HttpResponseRedirect('/home/')


def home(request):
    return render(request, 'homepage.html')


def vc(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from customerdetails')
        detail_tuple = cursor.fetchall()
        return render(request, 'vc.html', {'details': detail_tuple})


def about_us(request):
    return render(request, 'about.html')


def new_cus(request):
    if request.method == "GET":
        return render(request, 'form.html')
    elif request.method == "POST":
        id = request.POST['id']
        name = request.POST['name']
        email = request.POST['email']
        balance = request.POST['balance']
        with connection.cursor() as cursor:
            cursor.execute('select id from customerdetails')
            all_id = []
            for i in cursor.fetchall():
                all_id.append(i[0])
            if not id in all_id:
                cursor.execute('insert into customerdetails values(%s,%s,%s,%s)', (
                    id, name, email, balance))
            else:
                return HttpResponse('id should be unique')

        return HttpResponseRedirect('/transfer_money/')


def trans(request):
    if request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute('select name from customerdetails')
            cus_name = []
            for i in cursor.fetchall():
                cus_name.append(i[0])
            return render(request, 'transfer.html', {'customer_name': cus_name})
    elif request.method == "POST":
        sender = request.POST['Sender']
        receiver = request.POST['Receiver']
        amount = int(request.POST['amount'])
        with connection.cursor() as cursor:
            cursor.execute(
                "select balance from customerdetails where name = '%s'" % (sender))
            sender_balance = int(cursor.fetchall()[0][0])

        if int(sender_balance) >= int(amount):
            sender_new_balance = int(sender_balance) - int(amount)
            with connection.cursor() as cursor:
                update_sender_balance = "update customerdetails set Balance = %d where NAME = '%s'" % (
                    sender_new_balance, sender)
                cursor.execute(update_sender_balance)
                cursor.execute(
                    "select balance from customerdetails where name = '%s'" % (receiver))
                receiver_balance = cursor.fetchall()[0][0]
            receiver_new_balance = int(receiver_balance) + int(amount)
            with connection.cursor() as cursor:
                update_receiver_balance = "update customerdetails set Balance = %d where NAME = '%s'" % (
                    receiver_new_balance, receiver)
                cursor.execute(update_receiver_balance)
            with connection.cursor() as cursor:
                cursor.execute(
                    'insert into transactions (Sender,Receiver,Amount) values(%s,%s,%s)', (sender, receiver, amount))
            return HttpResponseRedirect('/trans_history/')
        else:
            return HttpResponseRedirect('/transfer_money/')


def transhistory(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from transactions')
        trans_tuple = cursor.fetchall()
        return render(request, 'trans.html', {'transaction': trans_tuple})
