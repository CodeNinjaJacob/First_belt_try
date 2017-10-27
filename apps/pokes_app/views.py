from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    if 'id' not in request.session:
        request.session['id'] = ''
    return render(request, 'pokes_app/index.html')

def home(request):
        if not request.session['id']:
            return redirect('/')
        else:
            current_user = User.objects.get(id = request.session['id'])
            context = {}
            context['current_user'] = current_user
            # User.objects.get(id = request.session['id']).alias
            context['received_pokes'] = current_user.poke_history
            context['friends'] = User.objects.exclude(id = request.session['id'])
            return render(request, 'pokes_app/home.html', context)

def addpoke(request, number):
    current_user = User.objects.get(id = request.session['id'])
    poked_person = User.objects.get(id = number)
    poked_person.poke_history += 1
    poked_person.save()
    Poke.objects.create(user=current_user, receiver=poked_person)
    return redirect('/pokes')
    
def register(request):
    name = request.POST['name']
    alias = request.POST['alias']
    email = request.POST['email']
    password = request.POST['password']
    birth_date = request.POST['birth_date']
    password_confirm = request.POST['password_confirm']
    data_input = {'name': name , 'alias': alias , 'email': email , 'password': password , 'password_confirm': password_confirm}
    errors = User.objects.validate_reg(data_input)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(name = name , alias = alias , email = email , password = hashed_password )
        request.session['id'] = User.objects.filter(email= request.POST['email'])[0].id
        return redirect('/pokes')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        user = User.objects.get(email = email)
        hash1 = user.password
    except:
        hash1 = '42'

    
    data_input = { 'email': email , 'password': password , 'hash1' : hash1}
    errors = User.objects.validate_log(data_input)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    else:
        request.session['id'] = User.objects.filter(email= request.POST['email'])[0].id
        return redirect('/pokes')




def logout(request):
    request.session.clear()
    return redirect('/')