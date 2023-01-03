from django.shortcuts import render, redirect
from .models import Post, Comment

# Create your views here.


def create_post(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == "POST":
            caption = request.POST.get("caption")
            image = request.FILES["image"]
            privacy = request.POST.get("privacy")


            # print(caption, image, privacy)

            post = Post.objects.create(user = user, caption= caption, image=image,privacy=privacy)
            post.save()
            return redirect('home')
            
        else:
            context = {
                'user' : user
            }
            return render(request, 'create.html',context)
    else:
        return redirect('signin')


def detail_post(request, pk):
    if request.user.is_authenticated:
        user = request.user
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        if request.method == "POST":
            user_comment = request.POST.get("comment")
            comment = Comment(user= user,post=post,comment=user_comment)
            comment.save()
            return redirect("post:detail_post",pk)
        else: 
            context = {
                'post' : post,
                'comments':comments,
            }
            return render(request, 'detail.html',context)
    else:
        return redirect('signin')

