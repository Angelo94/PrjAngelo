from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import requests
import csv
import psycopg2
from app.config import conn_str
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render

def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        if CheckIfUserAlreadyRegistered(email, name, password):
            allUser = selectAllUser()
            usrID = selectUserID(email, name, password)
            booking = createBookingList(usrID)
            vehiclesList = aviableVehicles()
            return render(request, 'app/home.html', { 'vehiclesList':vehiclesList, 'booking':booking, 'allUser':allUser ,'newuser':False,'name':name})
        else:
            CreateUserInDB(email, name, password)
            return render(request, 'app/login.html', {'msg':'user created, now just login'})
    else:
        return render(request, 'app/login.html', {'msg':'please create a user or login if you are already registered'})

def aviableVehicles():
    vehiclesList = []
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        selectVehicles= "SELECT * FROM vehicles ;"
        cursor.execute(selectVehicles)
        rows = cursor.fetchall()
        for car in rows:
            vehiclesList.append({ 'vehiclesID':car[0], 'code':car[1], 'model':car[2] })
        return vehiclesList
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
        return []      

def createBookingList(usrID):
    bookingList = []
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        selectBooking = "SELECT * FROM booking WHERE userID='%s';" % (usrID)
        cursor.execute(selectBooking)
        rows = cursor.fetchall()
        for booking in rows:
            model = bookedVehiclesName(booking[2])
            bookingList.append({'bookingID':booking[0], 'userID':booking[1], 'model':model, 'startDate':str(booking[3]), 'endDate':str(booking[4]), 'place':str(booking[5])  })
        return bookingList
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
        return []    

def bookedVehiclesName(vehiclesID):
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        selectModel = "SELECT model FROM vehicles WHERE vehiclesID='%s';" % (vehiclesID)
        cursor.execute(selectModel)
        rows = cursor.fetchall()
        return rows[0][0]
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
        return []      
    return vehiclesName

def selectUserID(email, name, password):
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        selectUsrs = "SELECT userID FROM users WHERE email='%s' and username='%s'and password='%s';" % (email, name, password)
        cursor.execute(selectUsrs)
        rows = cursor.fetchall()
        for r in rows:
            userID=r[0]
        return userID
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
        return []    

def selectAllUser():
    allUser = []
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        selectUsrs = "SELECT email, username FROM users;"
        cursor.execute(selectUsrs)
        rows = cursor.fetchall()
        for usr in rows:
            allUser.append(str(usr[1]) + "   " +str(usr[0])  )
        return allUser
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
        return []

def CheckIfUserAlreadyRegistered(email, name, password):
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        selectUsr = "SELECT username FROM users WHERE username='%s' and password='%s' and email='%s';" % (name, password, email)
        cursor.execute(selectUsr)
        rows = cursor.fetchall()
        if rows == []:
            return False
        else:
            return True
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
        return False

def CreateUserInDB(email, name, password):
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        insertUsr = "INSERT INTO users (email, username, password) VALUES ('%s','%s','%s');" % (email, name, password)
        cursor.execute(insertUsr)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
        return False
