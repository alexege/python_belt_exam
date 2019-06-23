from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Q
from .models import User, Trip

import bcrypt
from datetime import datetime, timedelta

# Landing Page: Localhost:8000/
def index(request):
    context = {
        'logged_in_users' : User.objects.all()
    }
    return render(request, "python_belt_exam_app/index.html", context)

#Register User: Localhost:8000/register
def register(request):

    #Validation Check
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        plain_text_password = request.POST['password']
        plain_text_conf_password = request.POST['confirmation_password']
        
        #Hash the plaintext password created
        hashed_password = bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())

        #If hashed password matches confirmation password, add user to db and move to success page
        if bcrypt.checkpw(plain_text_conf_password.encode(), hashed_password):
        
            #Add user to database if registration successful
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_password)
            
            #Set session user_key to id
            request.session['active_user'] = new_user.id
            return redirect('/dashboard')
        else:
            return redirect('/')

#Login User: Localhost:8000/login 
def login(request):

    #Validation Check
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        if User.objects.filter(email=request.POST['email']):
            user_email = request.POST['email']
            user_password = request.POST['password']

            login_user = User.objects.get(email=user_email)
            login_user_password = request.POST['password']

            passwords_match = bcrypt.checkpw(login_user_password.encode(), login_user.password.encode())
            if passwords_match:
                request.session['active_user'] = login_user.id
                print("Current user updated to: " + str(login_user.first_name) + str(login_user.last_name))
                return redirect('/dashboard')
            else:
                print("Invalid credentials")
                return redirect('/')
        else:
            return redirect('/')
    return redirect('/dashboard')

#Successful Login/Register: Localhost:8000/dashboard
def dashboard(request):

    #If an attempt is made to get to dashboard without logging in, redirect to landing page.
    if not 'active_user' in request.session:
        return redirect('/')

    #Mergingn queries. Interested to figure out an alternative way of doing this
    merged_queries = Trip.objects.filter(Q(created_by=request.session['active_user']) | Q(users_joined=request.session['active_user'])).order_by("-id")

    context = {
        'trip' : Trip.objects.all(),
        'merged_queries' : merged_queries,
        'current_user' : User.objects.get(id=request.session['active_user']),
        'trips_excluding_current_user' : Trip.objects.all().exclude(created_by=request.session['active_user']).exclude(users_joined=request.session['active_user']),
        'all_trips' : Trip.objects.all(),
    }
    return render(request, "python_belt_exam_app/success.html", context)

#Logout User: Localhost:8000/logout
def logout(request):
    del request.session['active_user']
    return redirect('/')


#Create new trip: Localhost:8000/trips/new
def create_new_trip(request):
    context = {
        'current_user' : User.objects.get(id=request.session['active_user']),
        'current_time' : str((datetime.now()).strftime("%Y-%m-%d")),
        'tomorrow'     : str((datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
    }
    return render(request, 'python_belt_exam_app/new_trip.html', context)

#add trip: Localhost:8000/add_trip
def add_trip(request):
    
    #Validation Check
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else:
        current_user_object = User.objects.get(id=request.session['active_user'])
        Trip.objects.create(destination=request.POST['destination'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], plan=request.POST['plan'], created_by=current_user_object)
        return redirect('/dashboard')

#Update trip: Localhost:8000/update_trip/<id>
def update_trip(request, id):

    errors = Trip.objects.update_trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/edit/' + id)
    else:
        trip_to_update = Trip.objects.get(id=id)
        trip_to_update.destination = request.POST['destination']
        trip_to_update.start_date = request.POST['start_date']
        trip_to_update.end_date = request.POST['end_date']
        trip_to_update.plan = request.POST['plan']
        trip_to_update.save()
        return redirect('/dashboard')


#Edit a trip: Localhost:8000/trips/edit/<id>
def edit_trip(request, id):
    context = {
        'my_trip' : Trip.objects.get(id=id),
        'current_user' : User.objects.get(id=request.session['active_user']),
        'trip' : Trip.objects.get(id=id).start_date.strftime("%Y-%m-%d"),
        'end_date' : Trip.objects.get(id=id).end_date.strftime("%Y-%m-%d"),
    }
    return render(request, 'python_belt_exam_app/edit_trip.html', context)

#View trip: Localhost:8000/trips/<id>
def view_trip(request, id):
    context = {
        'current_user' : User.objects.get(id=request.session['active_user']),
        'current_trip_object' : Trip.objects.get(id=id),
        'all_who_joined' : Trip.objects.get(id=id).users_joined.all().exclude(id=Trip.objects.get(id=id).created_by.id)
    }
    return render(request, 'python_belt_exam_app/view_trip.html', context)

#Join trip: Localhost:8000/join/<id>
def join_trip(request, id):
    Trip.objects.get(id=id).users_joined.add(User.objects.get(id=request.session['active_user']))
    return redirect('/dashboard')

#Remove trip: Localhost:8000/Remove/<id>
def remove_trip(request,id):
    Trip.objects.filter(id=id).delete()
    return redirect('/dashboard')

#Cancel trip: Localhost:8000/Cancel/<id>
def cancel_trip(request, id):
    Trip.objects.get(id=id).users_joined.remove(User.objects.get(id=request.session['active_user']))
    return redirect('/dashboard')