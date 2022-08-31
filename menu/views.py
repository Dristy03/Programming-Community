from django.http import request
from django.shortcuts import render, redirect
from account.models import Account
from user_profile.models import Profile


# sets the default view of Our Community.
def menu_view(request):
     return render(request, 'menu/menu_default.html')

# sets the Student's list of Our Community.
def menu_stdlist_view(request):
     if not request.user.is_authenticated:
        return redirect("welcome")
     else:
        context = {}
        account = Account.objects.all
        profile = Profile.objects.all
        context['account'] = account
        context['profile'] = profile
        return render(request, 'menu/menu_stdlist.html',context)

# sets the Teacher's list of Our Community.
def menu_tchlist_view(request):
     if not request.user.is_authenticated:
        return redirect("welcome")
     else:
        context = {}
        account = Account.objects.all
        profile = Profile.objects.all
        context['account'] = account
        context['profile'] = profile
        return render(request, 'menu/menu_tchlist.html', context)

# sets the About page of Our Community.
def about_view(request):
    if not request.user.is_authenticated:
        return redirect("welcome")
    else:
        return render(request, 'menu/about.html')