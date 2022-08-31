from django.shortcuts import get_object_or_404, render, redirect
from account.models import Account

from user_profile.forms import AccoutUpdateForm, ProfileUpdateForm
from user_profile.models import Profile
from post.models import Post


# Sets the profile view
def profile_view(request):
      user = request.user
      if not user.is_authenticated:
        return redirect("welcome")
      context={}
      if request.POST:
         print(request.POST)
         account_form = AccoutUpdateForm(request.POST or None,request.FILES or None,
                        instance=request.user)
         profile_form = ProfileUpdateForm(request.POST or None, instance=request.user)
         print(account_form.errors)
         print(profile_form.errors)
         if account_form.is_valid():
            print("account valid")
            obj = account_form.save()
            print(obj)
            account_form.initial = {
                  "first_name": request.POST['first_name'],
                  "last_name": request.POST['last_name'],
                  "image": obj.image,
                  'email': request.POST['email'],
            }
            context['account_form'] = account_form
         if profile_form.is_valid():
            print("profile valid")
            profile = get_object_or_404(Profile,user=user)
            if request.POST['department']:
               profile.department = request.POST['department']
            if request.POST.get('batch',None):
               profile.batch = request.POST['batch']
            if request.POST.get('reg_num',None):
               profile.reg_num = request.POST['reg_num']
            if request.POST['mobile_num']:
               profile.mobile_num = request.POST['mobile_num']
            if request.POST.get('designation',None):
               profile.designation = request.POST['designation']
            profile.save()
            print(profile)
            profile_form.initial = {
               "department": profile.department,
               "batch": profile.batch,
               "reg_num": profile.reg_num,
               "mobile_num": profile.mobile_num,
               "designation": profile.designation,

            }
            context ['profile_form'] = profile_form
         print(profile_form.initial)
         print(account_form.initial)
      else:
         print("get here")
         account = get_object_or_404(Account, pk=request.user.pk)
         profile = get_object_or_404(Profile, user=user)

         account_form = AccoutUpdateForm(
            initial={
               "first_name": account.first_name,
               "last_name": account.last_name,
               "image": account.image,
               'email': account.email,
            }
         )

         profile_form = ProfileUpdateForm(
            initial={
               "department": profile.department,
               "batch": profile.batch,
               "reg_num": profile.reg_num,
               "mobile_num": profile.mobile_num,
               "designation": profile.designation,
            }
         )
         print(profile_form.initial)
         print(account_form.initial)
         context ['profile_form'] = profile_form
         context['account_form'] = account_form
      posts = Post.objects.filter(author = user).order_by('-date_updated')
      context['posts'] = posts
      return render(request, 'user_profile/profile.html',context)