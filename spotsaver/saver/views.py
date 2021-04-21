from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import*

# Create your views here.

def index(request):
    return render(request, "index.html")

# Register
def register(request):
    if request.method=='POST':
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')


        user_pw=request.POST['pw']
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user=User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'],
        email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/main')
    return redirect('/')

# Login
def login(request):
    if request.method=='POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/main')
            else:
                messages.error(request, "Incorrect Password!")
        else:
            messages.error(request, "Email does not exist!")
    return redirect('/')

# Logout
def logout(request):
    request.session.clear()
    return redirect('/')
# main
def main(request):
    if 'user_id' not in request.session:
            return redirect('/')
    context = {
        "spots": Space.objects.all()
    }
    return render(request, "main.html", context)

def about(request):
    return render(request, "about.html")

def create_spot(request):
    if request.method == "POST":
        errors = Space.objects.validator(request.POST)
        if errors is not None and len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect("/adding")
        else:
            current_user = User.objects.get(id=request.session['user_id'])
            new_spot = Space.objects.create(location= request.POST["location"], description=request.POST["description"], spot_num=request.POST["spot_num"], author = current_user)
            current_user.spot.add(new_spot)
            return redirect ("/main")

def home_adding_spot(request):
    return render( request, "add_spot.html")

def back_home(request):
    if request.method=="POST":
        return redirect("/main")

def delete(request, id):
    space = Space.objects.get(id=id)
    space.delete()
    return redirect("/main")

def placeprofile(request, spot_id):
    context={
        'place':Space.objects.get(id= spot_id)

    }
    return render(request, 'profile.html', context)