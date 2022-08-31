from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.http import HttpResponse

# sets the contact us view
def contactusview(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("welcome")

    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        message += "\n \n \n \n"
        message += "Sender: " + str(user.first_name) +" "+ str(user.last_name) + "\n"
        message += "Sender Email: " + str(user.email) 
        context={}
        context['mail_sent'] = 0
        res = send_mail(subject,message,user.email,['sustprogrammingcommunity@gmail.com'],)
        if res == 1:
            context['mail_sent'] = 1
            return render(request, 'contact_us/contact_us.html', context)

    
    return render(request, 'contact_us/contact_us.html')