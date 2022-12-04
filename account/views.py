from django.shortcuts import render, redirect
from .models import CustomUser, Code, Profile
from django.contrib.auth.models import User
from post.models import Post
from django.utils import timezone
from .utility import send_email

from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        context = {
            "posts": posts,
        }
        return render(request, 'home.html',context)
    else:
        return redirect('signin')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            full_name = request.POST.get("fullname")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                user = None

            if user is not None:
                print("username already exits")
                return redirect(signup)
            else:
                new_user = CustomUser(username=username, email = email)
                new_user._full_name = full_name
                new_user.set_password(password)
                new_user.save()
                login(request, new_user)
                return redirect('home')
        else:
            return render(request, 'signup.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                request.session['pk'] = user.pk
                return redirect('verify')

            else:
                print("Wrong Username or password")
                return redirect('signin')
        else:
            return render(request, 'login.html')


def verify_code(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        try:
            pk = request.session.get('pk')
            user = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            user = None
        if user is not None:
            code = Code.objects.get(user=user)
            user_code_number = code.number
            sent_user_code = f"{user.username}: {user_code_number}"

            if not request.POST:
                print(sent_user_code)
                send_email(user.email,sent_user_code)
                return render(request, 'verify.html')
            else:
                user_given_code = request.POST.get('verify_code')
                if str(user_code_number) == user_given_code:
                    code.save()
                    login(request, user)
                    return redirect('home')
                else:
                    print("code didn't match")
                    code.save()
                    del request.session['pk']
                    request.session.modified = True
                    return redirect('signin')
        else:
            print("not allowed")
            return redirect('signin')


def user_logout(request):
    logout(request)
    return redirect('signin')
