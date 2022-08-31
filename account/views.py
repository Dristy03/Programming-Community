from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, authenticate, logout
from post.forms import CommentForm, CreatePostForm
from post.models import Notification, Post
from account.models import Account
from user_profile.models import Profile
from django.urls.base import reverse
from post.models import Post,get_post_queryset
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_text  
from django.core.mail import EmailMessage  
from .token import account_activation_token
from django.conf import settings
import requests
from account.forms import RegistrationForm, AccountAuthenticationForm

# views of the account app

# sends mail to verify the account
def send_verification_email(user,request):
    current_site = get_current_site(request)
    email_subject = "Activate your account"
    email_body = render_to_string('account/email_template.html',{
        'user' : user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    email = EmailMessage(subject=email_subject,body=email_body,from_email=settings.EMAIL_HOST_USER, to=[user.email])

    email.send()


# sets up the registration view
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST or None, request.FILES or None)
        # is valid check if the inputs are all correct
        if form.is_valid():

            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            form.save()
            account = authenticate(email=email, password=raw_password)
            Profile.objects.create(user = account)
            # email verification part 
            send_verification_email(account,request)
            #login(request, account)
             
            return render(request, "account/verfication_needed.html")
            
        else:  # Not correct input for form, so keep those data and show error
            context['registration_form'] = form

    else:  # GET request - create a black form
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

# sets up the welcome view
def welcome_view(request):
     user = request.user
     if user.is_authenticated:
        return redirect("home")
     return render(request, 'account/index.html')

# sets up the home view
def home_view(request):

    if not request.user.is_authenticated:
        return redirect("welcome")
    else:
        context = {}
        query=""
        if request.GET:
            query = request.GET.get('q','')
            context['query'] = str(query)
        blog_posts = sorted(get_post_queryset(query), key=attrgetter('date_updated'), reverse= True)
        

        response = requests.get("https://codeforces.com/api/contest.list?gym=false");
        data = response.json()
        result = data['result']
        cf_contest = [d for d in result if d['phase'] == 'BEFORE']
        cf_contest.sort(key= lambda x : x['startTimeSeconds'])
        #pagination
        page = request.GET.get('page',1)
        post_per_page = 5
        posts_paginator = Paginator(blog_posts,post_per_page)
        try:
            blog_posts= posts_paginator.page(page)
        except PageNotAnInteger:
            blog_posts = posts_paginator.page(post_per_page)
        except EmptyPage:
            blog_posts = posts_paginator.page(posts_paginator.num_pages)
        context['blog_posts'] = blog_posts
        context['cf_contests'] = cf_contest


        # post form test 
        form = CreatePostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            author = Account.objects.filter(email=request.user.email).first()
            obj.author = author
            obj.save()
            for account in Account.objects.all():
                if account.email == author.email:
                    continue
                Notification.objects.create(
                    notification_type=1, from_user=author, to_user=account, post=obj)

            form = CreatePostForm()
        context['form'] = form
        return render(request, 'account/home.html', context)

# sets up the login view
def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user and user.is_email_verified:
                login(request, user)
                return redirect("home")
            else:
                context['failure_message'] = "Sorry, the user is not verified.Please check your email"

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "account/login.html", context)

# sets up the logout view
def logout_view(request):
    logout(request)
    return redirect('/')


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid) 
        print(uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None 
    print(user)
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_email_verified = True  
        user.save()
        return render(request,"account/email_confirmed.html")
    else:
        return render(request, "account/verification_failed.html" )