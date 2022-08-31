from time import time
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.views import View
from post.forms import CommentForm, CreatePostForm
from account.models import Account
from post.models import Comment, Notification, Post
from datetime import datetime

# sets the create view of post
def create_post_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('welcome')

    form = CreatePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        for account in Account.objects.all():
            if account.email == author.email:
                continue
            Notification.objects.create(
                notification_type=1, from_user=author, to_user=account, post=obj)

        form = CreatePostForm()
        return redirect('home')

    context['form'] = form

    return render(request, "post/create_post.html", context)

# sets up the edit view of post
def edit_post_view(request,pk):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('welcome')

    form = CreatePostForm(request.POST or None, request.FILES or None)
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST' and form.is_valid():
        post.text = request.POST.get('text')
        post.date_updated = datetime.now()
        post.save()
        form = CreatePostForm()
        return redirect('home')
    form.initial={
        'text': post.text,
    }
    context['form'] = form

    return render(request, "post/create_post.html", context)


# sets up the delete view of post
def delete_post_view(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('home')
    

# sets up the details view of post
class PostDetailsView(View):
    def get(self,request,pk,*args, **kwargs):
        post = Post.objects.get(pk=pk)
        context ={'post':post}
        return render(request,'post/post_detail.html',context)

# sets up the add comment view of the post
def add_comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST,request.FILES )
        print(form.errors)
        if form.is_valid():
            print("comment valid")
            print(request.POST)
            print(request.FILES)
            # comment = form.save()
            # comment.post = post
            # comment.author = request.user
            # if request.POST.get('image',None):
            #     comment.image = request.POST['image']
            body = form.cleaned_data.get('body')
            image = None
            if request.FILES.get('comment_image',None):
                image = form.cleaned_data.get('comment_image')
            comment =Comment.objects.create(body=body,post=post,author = request.user,comment_image= image)
            comment.save()
            Notification.objects.create(
                notification_type=2, from_user=comment.author, to_user=post.author, post=post)
            return redirect('post_details',pk)
    else:
        form = CommentForm()
    return redirect('post_details',pk=pk)


# handles the mark all read functionality of notification
class mark_all_notification(View):
    def get(self,request,*args, **kwargs):
        notifications = Notification.objects.filter(to_user= request.user)
        for notification in notifications:
            notification.user_has_seen = True
            notification.save()
        return redirect('home')

# sets post notification view
class PostNotificationView(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect('post_details',pk=post_pk)



