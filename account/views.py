from django.shortcuts import render, redirect
from .models import CustomUser, Code, Profile, UserRequestIP
from django.contrib.auth.models import User
from post.models import Post
from django.utils import timezone
from .utility import send_email, get_client_ip, secure_password
from axes.utils import reset
from axes.models import AccessAttempt
import datetime
from dateutil import parser
from itertools import chain
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user_reqest_ip_obj = UserRequestIP.objects.filter(user = request.user)
        if not user_reqest_ip_obj :
            ip = get_client_ip(request)
            user_request_ip = UserRequestIP(user = request.user, ip_address = ip, path_info = request.path)
            user_request_ip.save()
        else:
            user_request_ip = user_reqest_ip_obj[0]
            timenow = datetime.datetime.now(timezone.utc)
            user_last_attempt = user_request_ip.attempt_time
            difference = timenow-user_last_attempt
            minutes = difference.total_seconds() / 60
            print('Total difference in minutes: ', minutes)

            if minutes < 1 and user_request_ip.attempt_numbers == 50:
                logout(request)
                user_request_ip.attempt_numbers = 0
                user_request_ip.save()
                return redirect('signin')     
            elif minutes > 5 and user_request_ip.attempt_numbers >= 50:
                user_request_ip.attempt_numbers = 0
                user_request_ip.save()               
            else:
                user_request_ip.attempt_numbers += 1
                user_request_ip.save()

        posts = Post.objects.filter(privacy=1) | Post.objects.filter(privacy=2)
        
        user_posts = []
        user_profile = Profile.objects.get(user = request.user)

        for post in posts:
            if post.user in user_profile.followers.all():
                user_posts.append(post)
        for post in posts:
            if post.privacy == "1":
                user_posts.append(post)

        context = {
            "posts": user_posts,
        }
        return render(request, 'home.html',context)
    else:
        return redirect(signin)





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
                is_password_okay = secure_password(password)
                if is_password_okay is True:
                    new_user = CustomUser(username=username, email = email)
                    new_user._full_name = full_name
                    new_user.set_password(password)
                    new_user.save()
                    login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('home')
                else:
                    messages.add_message(request, messages.INFO, 'Password must contains atleast one lowercase, uppercase,digit and spacial character and password must be atleast 8 digit long')
                    return redirect("signup")
        else:
            return render(request, 'signup.html')

def remove_block(username):
    try:
        user = AccessAttempt.objects.get(username = username)
        if user is not None:
            timenow = datetime.datetime.now(timezone.utc)
            user_last_attempt = user.attempt_time
            difference = timenow-user_last_attempt
            minutes = difference.total_seconds() / 60
            print('Total difference in minutes: ', minutes)
            if minutes > 5:
                reset(username=username)
        else:
            pass
    except:
        pass

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            remove_block(username)
            user = authenticate(request=request,username=username, password=password)
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
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
