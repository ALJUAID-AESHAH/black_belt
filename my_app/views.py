from django.shortcuts import render, redirect
from .models import User, Wish
from django.contrib import messages
import bcrypt


def index(request):
    return render(request,'index.html')

def dashboard(request):
    user=User.objects.get(id=request.session['id'])
    context={
        'user':User.objects.get(id=request.session['id']),
        'wishes':user.wishes.order_by("-created_at"),
        'all_wishes_granted': Wish.objects.filter(granted=True),
        'all_wish_not_belong_to_user': Wish.objects.exclude(wisher=User.objects.get(id=request.session['id']))
    }
    return render(request,'dashboard.html',context)

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print('hash',pw_hash)
        user=User.objects.create(first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        hashed_password=pw_hash)
        request.session['id'] = user.id
        return redirect('/wishes')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        return redirect('/wishes')

def logout(request):
    request.session.flush()
    return redirect('/')

def new_wish(request):
    context={
        'user':User.objects.get(id=request.session['id']),
    }
    return render(request,'new.html',context)

def create_wish(request):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        Wish.objects.create(name=request.POST['name'],desc=request.POST['desc'],
        wisher=User.objects.get(id=request.session['id']))
        return redirect('/wishes')

def delete_wish(request,wish_id):
    Wish.objects.get(id=wish_id).delete()
    return redirect('/wishes')

def edit_wish(request,wish_id):
    context={
        'wish':Wish.objects.get(id=wish_id),
        'user':User.objects.get(id=request.session['id']),
    }
    return render(request,'edit.html',context)

def update(request,wish_id):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'edit/{wish_id}')
    else:
        update=Wish.objects.get(id=wish_id)
        update.name=request.POST['name']
        update.desc=request.POST['desc']
        update.save()
        return redirect('/wishes')

def mark_wish_as_granted(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish.granted = True
    wish.save()
    return redirect('/wishes')

def cancel(request):
    return redirect('/wishes')

def mark_wish_as_favorite(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session['id'])
    user.favorites.add(wish)
    return redirect('/wishes')

def state(request):
    user_wish=Wish.objects.filter(wisher=User.objects.get(id=request.session['id']))
    context={
        'user':User.objects.get(id=request.session['id']),
        'granted_wish':Wish.objects.filter(granted=True),
        'user_granted_wish': user_wish.filter(granted=True),
        'user_pending_wish': user_wish.filter(granted=False),
    }
    return render(request,'state.html',context)


