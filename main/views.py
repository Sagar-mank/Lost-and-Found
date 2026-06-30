from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import LostItem, FoundItem, Claim
from django.contrib import messages

def home(request):
    lost_items = LostItem.objects.filter(claimed=False)[:6]
    return render(request, 'home.html', {'lost_items': lost_items})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm_password']
        if password == confirm:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Passwords don't match")
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def report_lost(request):
    if request.method == 'POST':
        LostItem.objects.create(
            user=request.user,
            name=request.POST['name'],
            description=request.POST['description'],
            location=request.POST['location'],
            date_lost=request.POST['date_lost'],
            contact=request.POST['contact']
        )
        messages.success(request, "Lost item reported successfully!")
        return redirect('home')
    return render(request, 'report_lost.html')

@login_required
def report_found(request):
    if request.method == 'POST':
        FoundItem.objects.create(
            user=request.user,
            name=request.POST['name'],
            description=request.POST['description'],
            location=request.POST['location'],
            date_found=request.POST['date_found'],
            contact=request.POST['contact']
        )
        messages.success(request, "Found item reported successfully!")
        return redirect('home')
    return render(request, 'report_found.html')

def lost_items_list(request):
    items = LostItem.objects.filter(claimed=False)
    return render(request, 'lost_items.html', {'items': items})

@login_required
def claim_item(request, item_id):
    item = get_object_or_404(LostItem, id=item_id)
    if request.method == 'POST':
        Claim.objects.create(
            lost_item=item,
            claimed_by=request.user,
            message=request.POST['message'],
            status='Pending'
        )
        messages.success(request, "Claim submitted successfully!")
        return redirect('lost_items')
    return render(request, 'claim_item.html', {'item': item})