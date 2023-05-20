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
        d['flights']=flights
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
        flight_groups = Flight.objects.annotate(num_bookings=Count('flight_book'))
        d={}
        d['flights']=flight_groups
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
        if request.method == 'POST':
            Flight_Book.objects.create(flight=flight, user=User.objects.get(id=temp))
            flight.seats_booked+=1
            flight.save()
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
        for i in flights:
            f=Flight.objects.get(flight_number=i.flight_number)
            if Flight_Book.objects.filter(user=u, flight=f) or f.seats_booked==f.number_of_seats:
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
        f=Flight_Book.objects.filter(user=User.objects.get(id=temp))
        flights=[]
        for i in f:
            flights.append(i.flight)
        d['flights']=flights
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
                f'You have successfully created an account. Click this link to verify your email: {verification_url}\n\nRegards,\nTeam Recharge',
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
            flight.delete()
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
    