from django.shortcuts import render, redirect
from .models import CustomUser, Code, Profile
from post.models import Post
from django.utils import timezone

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
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            print("username already exits")
            return redirect(signup)
        else:
            new_user = CustomUser(username=username, phone_number=phone)
            new_user.set_password(password)
            new_user.save()
            login(request, new_user)
            return render(request, 'home.html')
    else:
        return render(request, 'signup.html')


def signin(request):
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
    try:
        pk = request.session.get('pk')
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        user = None
    if user is not None:
        code = Code.objects.get(user=user)
        user_code_number = code.number
        sent_user_code = f"{user.username}: {user_code_number}"

        if not request.POST:
            print(sent_user_code)
            return render(request, 'verify.html')
        else:
            user_given_code = request.POST.get('verify_code')
            if str(user_code_number) == user_given_code:
                code.save()
                login(request, user)
                return redirect('home')
            else:
                print("code didn't match")
                del request.session['pk']
                return redirect('signin')
    else:
        print("not allowed")
        return redirect('signin')
