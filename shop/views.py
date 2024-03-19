from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
import json
from cart.cart import Cart
# Create your views here.


def search(request):
    #define if the form was filled
    if request.method == "POST":
        search_result = request.POST["search"]
    #query products from db in filter use 'icontains' for case insensitive search
        search_result = Product.objects.filter(Q(name__icontains=search_result) | Q(description__icontains=search_result)) 
        if not search_result:
             messages.success(request, ("There is nothing here for that query!"))
             return render(request, 'search.html',{})
        else:     
            return render(request, 'search.html',{"search":search_result})
    else:
        return render(request, 'search.html',{})



def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})


def about(request):
    return render(request, 'about.html',{})


def login_user(request):
    
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Shoping cart persistance logic

            current_user = Profile.objects.get(user__id=request.user.id)
            #get saved cart from db
            saved_cart = current_user.old_cart
            #convert db string to python dict
            if saved_cart:
                #convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #add the loaded cart dictionary to user session
                #get cart
                cart = Cart(request)
                #loop through the cart and add the items from the db
                for key, value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)


            messages.success(request, ("You have been logged in successfully!!!"))
            return redirect('home')
        else:
            messages.success(request, ("An error occured! Please Try again!"))
            return redirect('home')
    else:
        return render(request, 'login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out successfully!!!"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been registered successfully, add your billing information below"))
            return redirect('update_info')
        else:
            messages.success(request, ("Error occured while registration!"))
            return redirect('home') 
    else:
        return render(request, 'register.html',{'form':form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        #instance parameter helps to maintain data of current user inside the form
        update_form = UpdateUserForm(request.POST or None, instance=current_user)
        if request.method == "POST":
            if update_form.is_valid():
                update_form.save()
                login(request, current_user)
                messages.success(request, ("User has been updated successfully!!!"))
                return redirect('home') 
        return render(request, 'update_user.html',{'update_form':update_form})
    else:
        messages.success(request, ("Login first to access this page!!!"))
        return redirect('home')



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password is Updated Successfully")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html',{'form':form})
    else:
        messages.success(request, ("Login first to access this page!!!"))
        return redirect('home')   


def update_info(request):
    if request.user.is_authenticated:
        current_user_profile = Profile.objects.get(user__id=request.user.id)
        #instance parameter helps to maintain data of current user inside the form
        form = UserInfoForm(request.POST or None, instance=current_user_profile)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                
                messages.success(request, ("Your Information has been updated successfully!!!"))
                return redirect('home') 
        return render(request, 'update_info.html',{'form':form})
    else:
        messages.success(request, ("Login first to access this page!!!"))
        return redirect('home')



def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'product':product})

def category(request, foo):
    # replace hyphens with spaces
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html',{'products':products, 'category':category})
    except:
        messages.success(request, ("Error category does not exist!"))
        return redirect('home') 
    
    
    return render(request, 'product.html',{'product':product})


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html',{'categories':categories})
  