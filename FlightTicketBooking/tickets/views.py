from django.shortcuts import render, redirect, HttpResponse
from .models import *
import datetime,jwt
import traceback  
from django.contrib.auth.hashers import check_password
from .forms import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
from django.db.models import Count

from django.db import models
from django.apps import apps


def addflight(request):
    try:
        token = request.COOKIES.get('jwt')
        if not token:
            print(token)
            return redirect("login")
        
        try:
            payload = jwt.decode(token, 'devrev@123', 'HS256')
        except jwt.ExpiredSignatureError as e:
            print(traceback.exc())
            return redirect("adminlogin")
        temp=payload['id']
        if temp!='admin':
            return redirect('adminlogin')
        if request.method == 'POST':
            form = FlightForm(request.POST)
            if form.is_valid():
                form.save()
                flight=Flight.objects.get(flight_number=form['flight_number'].value())
                return redirect("adminprofile")
        else:
            form = FlightForm()
        return render(request, 'addflight.html', {'form': form})
    except Exception as e:
        print(e)
        return HttpResponse("Some error occurred")

def adminlogin(request):
    try:
        d={}
        d["username"]=""
        d["password"]=""
        d["show"]=0
        if request.method=="POST":
            username=request.POST.get("username")
            password = request.POST.get("password")
            d["username"]=username
            d["password"]=password
            if username=='admin' and password=='admin':

                payload = {
                    'id':username,
                    'exp':datetime.datetime.utcnow() + datetime.timedelta(days=60),
                    'iat':datetime.datetime.utcnow()
                }

                token = jwt.encode(payload, 'devrev@123', algorithm='HS256')
                response = redirect("adminprofile")

                response.set_cookie(key='jwt', value=token, httponly=True)
                
                return response

            else:
                d["show"]=1
                return render(request,"adminlogin.html", d)
        return render(request, "adminlogin.html", d)
    except Exception as e:
        print(e)
        return HttpResponse("Some error occurred")
    

def adminprofile(request):
    try:
        token = request.COOKIES.get('jwt')
        if not token:
            print(token)
            return redirect("login")
        
        try:
            payload = jwt.decode(token, 'devrev@123', 'HS256')
        except jwt.ExpiredSignatureError as e:
            print(traceback.exc())
            return redirect("adminlogin")
        temp=payload['id']
        if temp!='admin':
            return redirect('adminlogin')
        d={}
        d['name']="Admin"
        # Flight.objects.filter(takeoff_date_gt='input_date')
        flights = Flight.objects.all()
        active_flights=[]
        for flight in flights:
            if flight.active:
                active_flights.append(flight)
        d['flights']=active_flights
        return render(request, "adminprofile.html", d)
    except Exception as e:
        print(e)
        return HttpResponse("Some error occurred")
    
def adminview(request):
    try:
        token = request.COOKIES.get('jwt')
        if not token:
            print(token)
            return redirect("login")
        
        try:
            payload = jwt.decode(token, 'devrev@123', 'HS256')
        except jwt.ExpiredSignatureError as e:
            print(traceback.exc())
            return redirect("adminlogin")
        temp=payload['id']
        if temp!='admin':
            return redirect('adminlogin')
        # flight_groups = Flight.objects.annotate(num_bookings=Count('flight_book')) #need to change
        d={}
        flights_all=Flight.objects.all()
        flights=[]
        passenger={}
        for flight in flights_all:
            if flight.active:
                flights.append(flight)
                pas=Booking.objects.filter(flight=flight)
                for p in pas:
                    if flight.flight_number in passenger:
                        passenger[flight.flight_number].append(p.passenger_name)
                    else:
                        passenger[flight.flight_number]=[p.passenger_name]    
        d['flights']=flights
        d["passengers"]=passenger
        print(d)
        return render(request, 'adminview.html',d)
    except Exception as e:
        print(e)
        return HttpResponse("Some error occurred")

def bookflight(request, flight_id):
    try:
        token = request.COOKIES.get('jwt')
        if not token:
            print(token)
            return redirect("login")
        
        try:
            payload = jwt.decode(token, 'devrev@123', 'HS256')
        except jwt.ExpiredSignatureError as e:
            print(traceback.exc())
            return redirect("login")
        temp=payload['id']
        if temp=='admin':
            return redirect('adminprofile')
        flight = Flight.objects.get(pk=flight_id)
        if(request.method=="GET"):
            d={}
            d['flight']=flight
            n=request.GET.get("no_of_seats")
            seat_counter=[i for i in range(1,int(n)+1)]
            d['no_seats']=seat_counter
            d['limit']=n
            print("limit",d['limit'])
            reserved_seats=[]
            reserved_seats_list=Booking.objects.filter(flight=flight)
            for s in reserved_seats_list:
                reserved_seats.append(s.seat_number)
            print("reserved Seats : ",reserved_seats)
            d["reserved_seats"]=reserved_seats
            return render(request,"confirmticket.html",d)
        else:
            # selected_seats = request.POST.getlist('checkbox_name')
            d={}
            selected_seats=[]
            my_list = ''
            if 'selected_seats' in request.POST:
                my_list = request.POST.get("selected_seats")
            my_list = my_list.replace(',',' ')
            for j in my_list.split():
                selected_seats.append(j)
            n=request.POST.get("n")
            passenger_names=[]
            booked_seats=[]
            print(n,len(selected_seats))
            print(selected_seats)
            if(len(selected_seats)!=int(n)):
                d["message"]="Please select required seats"
                return render(request,"confirmticket.html",d)
            for i in range(1,int(n)+1):
                p_name="name"+str(i)
                passenger_names.append(request.POST.get(p_name))
            for ind,seat in enumerate(selected_seats):
                if(Booking.objects.filter(flight=flight,seat_number=seat)):
                    d['message']="selected seats already booked"
                    return render(request,"confirmticket.html",d)
                else:
                    seat_price=flight.price_business
                    seat_class="business"
                    if(int(seat[0])>3):
                        seat_price=flight.price_economy
                        seat_class="economy"
                    Booking.objects.create(flight=flight,seat_number=seat,seat_status="reserved",seat_price=float(seat_price),seat_class=seat_class,passenger_name=passenger_names[ind],user=User.objects.get(id=temp))
                    print("Seats booked",seat)
                    booked_seats.append(seat)
            # Booking.objects.create(flight=flight, user=User.objects.get(id=temp))
            flight.available_seats-=len(booked_seats)
            flight.save()
            email=User.objects.get(id=temp).email
            u_name = User.objects.get(id=temp).name
            print(u_name)
            content="Dear "+u_name+",\nWe are delighted to inform you that your ticket booking has been successfully confirmed. Thank you for choosing our services for your upcoming travel. This email serves as a confirmation of your booking details.\n\nBooking Details:\nAirline:"+flight.flight_name+"\nFlight Number:"+flight.flight_number+"\nDeparture Airport:"+flight.flight_from+"\nArrival Airport:"+flight.flight_to+"\nDeparture Date:"+str(flight.takeoff_date)+"\nDeparture Time:"+str(flight.takeoff_time)+"\n\nTicket Info:\n"
            indi=0
            for p in passenger_names:
                content+="Name : "+p+" , "+"Seat No.:"+selected_seats[indi]+"\n"
                indi+=1
            content+="\n\nRegards,\nAirDev"
            print(content)
            print(email)
            send_mail(
                'Your AirDev ticket has been confirmed!',
                content,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        return redirect('profile')

    except Exception as e:
        print(e)
        return HttpResponse("Some error occurred")
    

def buyticket(request):
    try:
        token = request.COOKIES.get('jwt')
        if not token:
            print(token)
            return redirect("login")
        
        try:
            payload = jwt.decode(token, 'devrev@123', 'HS256')
        except jwt.ExpiredSignatureError as e:
            print(traceback.exc())
            return redirect("login")
        temp=payload['id']
        if temp=='admin':
            return redirect('login')
        u=User.objects.get(id=temp)
        d={}
        flights = Flight.objects.all()
        print(flights)
        if request.method=="GET":
            date_greater = request.GET.get('date_greater')
            date_less = request.GET.get('date_less')
            time_greater = request.GET.get('time_greater')
            time_less = request.GET.get('time_less')
            d["date_greater"]=date_greater
            d["date_lesser"]=date_less
            d["time_greater"]=time_greater
            d['time_lesser']=time_less
            filter_conditions = Q()
            if date_greater:
                filter_conditions &= Q(takeoff_date__gt=date_greater)
            if date_less:
                filter_conditions &= Q(takeoff_date__lt=date_less)
            if time_greater:
                filter_conditions &= Q(takeoff_time__gt=time_greater)
            if time_less:
                filter_conditions &= Q(takeoff_time__lt=time_less)
            flights=flights.filter(filter_conditions)
        lst=[]
        curr_date = datetime.datetime.now()
        cyear=curr_date.year
        cmonth=curr_date.month
        cday=curr_date.day
        for i in flights:
            f=Flight.objects.get(flight_number=i.flight_number)
            if(f.takeoff_date.month<=cmonth and  f.takeoff_date.year<=cyear and f.takeoff_date.day<cday):
                f.active=False
                f.save()
            if (not f.active) or Booking.objects.filter(user=u, flight=f) or f.available_seats<=0 or (f.takeoff_date.month<=cmonth and  f.takeoff_date.year<=cyear and f.takeoff_date.day<cday ):
                continue
            lst.append(i)
        d['flights']=lst
        return render(request, "buyticket.html", d)
    except Exception as e:
        print(e)
        return HttpResponse("Some error occurred")
    
def login(request):
    try:
        d={}
        d["email"]=""
        d["password"]=""
        d["show"]=0
        if request.method=="POST":
            email=request.POST.get("email")
            password = request.POST.get("password")
            d["email"]=email
            d["password"]=password
            temp = User.objects.filter(email=email, is_verified=True)
            print(temp)
            if temp:
                print(temp[0])
                if check_password(password,temp[0].password):

                    payload = {
                        'id':temp[0].id,
                        'exp':datetime.datetime.utcnow() + datetime.timedelta(days=60),
                        'iat':datetime.datetime.utcnow()
                    } 

                    token = jwt.encode(payload, 'devrev@123', algorithm='HS256')
                    response = redirect("profile")

                    response.set_cookie(key='jwt', value=token, httponly=True)
                    
                    return response
                else:
                    d["show"]=1
                    return render(request,"login.html", d)

            else:
                d["show"]=1
                return render(request,"login.html", d)

        else:
            return render(request,"login.html", d)
        return render(request,"login.html", d)
    except Exception as e:
        print(traceback.exc())
        return HttpResponse("<h1>Unexpected Error</h1>")

def logout(request):
    try:
        response = redirect("login")
        response.delete_cookie('jwt')
        return response
    except Exception as e:
        print(e)
        return HttpResponse("Some error occurred")

def profile(request):
    try:
        token = request.COOKIES.get('jwt')
        if not token:
            print(token)
            return redirect("login")
        
        try:
            payload = jwt.decode(token, 'devrev@123', 'HS256')
        except jwt.ExpiredSignatureError as e:
            print(traceback.exc())
            return redirect("login")
        temp=payload['id']
        if temp=='admin':
            return redirect('login')
        temp1 = User.objects.get(id=temp)
        d={}
        d['name']=temp1.name
        f=Booking.objects.filter(user=User.objects.get(id=temp))
        flights=set()
        seats={}
        amounts={}
        for i in f:
            if(not i.flight.active):
                continue
            total_amount=0.00
            tem=Booking.objects.filter(user=User.objects.get(id=temp),flight=i.flight)
            flights.add(i.flight)
            seat_no=""
            f_num=i.flight.flight_number
            print(tem)
            for s_ in tem:
                seat_no+=s_.seat_number+","
                print(float(s_.seat_price))
                total_amount+=float(s_.seat_price)
            seats[f_num]=seat_no[:-1]
            amounts[i.flight.flight_number]=total_amount
        d['flights']=flights
        d['seats']=seats
        d['total_amounts']=amounts
        flights=list(flights)
        print(d)
        return render(request, "profile.html", d)
    except Exception as e:
        print(e)
        return HttpResponse("Some error occurred")

def register(request):
    print("Register")
    d={}
    try:
        d["name"]=""
        d["regno"]=""
        d["year"]=""
        d["dept"]=""
        d["email"]=""
        d["password"]=""
        d["college"]=""
        d["confirmpassword"]=""
        d["show"]=0
        d["message"]=""
        if request.method=="POST":
            print("Inner123 Register")
            name = request.POST.get("name").strip()
            age = request.POST.get("age").strip()
            contactno = request.POST.get("contactno").strip()
            email = request.POST.get("email").strip()
            password = request.POST.get("password").strip()
            confirmpassword = request.POST.get("confirmpassword").strip()
            d["name"]=name
            d["age"]=age
            d["contactno"]=contactno
            d["email"]=email
            d["password"]=password
            d["confirmpassword"]=confirmpassword
            d["message"]=""
            temp = User.objects.filter(email=email)
            message=None
            if password and  len(password)<8:
                message="Password length should be greater than 8"
            elif not name or not age or not contactno or not email or not password:
                message="Please fill all the fields"
            elif len(name)>50 or len(age)>2 or len(contactno)>20 or len(email)>200 or len(password)>20:
                message="Field lengths should not cross the limit"
            elif password!=confirmpassword:
                message="Password does not match confirm password"
            d["message"]=message
            if message:
                return render(request, "register.html", d)
            if temp:
                d["show"]=1
                return render(request, "register.html",d)
            verification_token = get_random_string(length=32)
            verification_url = request.build_absolute_uri(reverse('verify_email')) + f'?token={verification_token}&email={email}'
            User.objects.create(name=name, email=email, password=password, contactno=contactno, age=age, token=verification_token, is_verified=False)
            send_mail(
                'Verify your email',
                f'You have successfully created an account. Click this link to verify your email: {verification_url}\n\nRegards,\nAirDev',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            return redirect("login")
        return render(request, "register.html",d)
    except Exception as e:
        print(e)
        d["show"]=2
        return render(request, "register.html", d)

def removeflight(request, flight_id):
    try:
        token = request.COOKIES.get('jwt')
        if not token:
            print(token)
            return redirect("login")
        
        try:
            payload = jwt.decode(token, 'devrev@123', 'HS256')
        except jwt.ExpiredSignatureError as e:
            print(traceback.exc())
            return redirect("adminlogin")
        temp=payload['id']
        if temp!='admin':
            return redirect('adminlogin')
        flight = Flight.objects.get(pk=flight_id)
        if request.method == 'POST':
            curr_date = datetime.datetime.now()
            cyear=curr_date.year
            cmonth=curr_date.month
            cday=curr_date.day
            f=flight
            print(f,f.takeoff_date.month,f.takeoff_date.year,f.takeoff_date.day)
            print(cmonth,cyear,cday)
            if(f.takeoff_date.month>=cmonth and  f.takeoff_date.year>=cyear and f.takeoff_date.day>=cday):
                use=Booking.objects.filter(flight=flight)
                users=set()
                print("INsied")
                emails=[]
                for i in use:
                    users.add(i.user)
                for p in users:
                    emails.append(p.email)
                content="We regret to inform you that your upcoming flight has been cancelled. We understand the inconvenience this may cause and would like to provide you with the necessary information regarding the cancellation.Refund will be initiated within 24hours\nFlight Details:\nAirline:"+flight.flight_name+"\nFlight Number:"+flight.flight_number+"\n\nRegards,\nAirDev"
                print(emails)
                send_mail(
                    'Flight Cancellation Notification',
                    content,
                    settings.EMAIL_HOST_USER,
                    emails,
                    fail_silently=False,
                )
            flight.active=False
            flight.save()
        return redirect('adminprofile')
    except Exception as e:
        print(e)
        return HttpResponse("Some error occurred")
    
    
def verify_email(request):
    try:
        token = request.GET.get('token')
        email = request.GET.get('email')
        if not token:
            return HttpResponse('<h1>Verification Failed</h1>')
        temp = User.objects.get(email=email)

        if not temp:
            return HttpResponse('<h1>Verification Failed</h1>')
        
        if temp.is_verified:
            return HttpResponse("<h1>Already Verified</h1>")

        if temp.token != token:
            return HttpResponse('<h1>Verification Failed</h1>')

        temp.is_verified = True
        temp.save()

        # return HttpResponse('<h1>Successfully Verified Mail Now you can go login and go to the app</h1>')
        return redirect("login")
    except:
        return HttpResponse('<h1>Verification Failed</h1>')
    