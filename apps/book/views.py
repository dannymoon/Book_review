from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'book/index.html')

def add_user(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for error in errors.itervalues():
                messages.error(request, error)
            return redirect('/')
        else:
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed_password)
            messages.error(request, "Successfully Registered")
            return redirect('/')

def login(request):
    if request.method == 'POST':
        if not 'login_status' in request.session:
            request.session['login_status'] = False
        login_data = User.objects.filter(username=request.POST['username'])
        inputted_password = request.POST['password']
        stored_password = User.objects.filter(username=request.POST['username']).first().password
        if login_data and bcrypt.checkpw(inputted_password.encode(), stored_password.encode()):
            request.session['login_status'] = {'id':login_data.first().id, 'name':login_data.first().name, 'username':login_data.first().username}
            print request.session['login_status']
            return redirect('/wishlist')
        else:
            messages.error(request, "Email and password does not match")
            return redirect('/')

def logout(request):
    request.session['login_status'] = False
    return redirect('/')

def wishlist(request):
    items = Item.objects.all()
    items_belong_this = Item.objects.all()
    print items_belong_this
    context = {
        'items':items,
        'items_belong_this': items_belong_this
    }
    return render(request, 'book/wish_list.html', context)

def add_item(request):
    return render(request, 'book/add_item.html')

def add(request):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['login_status']['id'])
        temp = Item.objects.create(itemname=request.POST['item_name'], added_by=this_user)
        temp.wished_by.add(this_user)
    return redirect('/wishlist')

def add_to_wishlist(request):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['login_status']['id'])
        this_item = Item.objects.get(id=request.POST['item_id'])
        this_item.wished_by.add(this_user)
    return redirect('/wishlist')

def remove_from_wishlist(request):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['login_status']['id'])
        this_item = Item.objects.get(id=request.POST['item_id'])
        this_item.wished_by.remove(this_user)
    return redirect('/wishlist')

def delete_item(request):
    if request.method == 'POST':
        Item.objects.get(id=request.POST['item_id']).delete()
    return redirect('/wishlist')

def display_item(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {
        'item':item
    }
    return render(request, 'book/item_detail.html', context)