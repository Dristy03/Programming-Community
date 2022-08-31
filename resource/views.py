from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View
from django.http import HttpResponse
from resource.forms import ResourceForm
from account.models import Account  
from resource.models import Resource, get_resource_queryset
from operator import attrgetter



# sets up the resource view

def resource_view(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("welcome")
    else:
        if request.method == 'POST' and request.FILES["resourcefile"]:
            print(request.FILES)
            form = ResourceForm(request.POST, request.FILES)
            
            print(form.errors)
            if form.is_valid():
                document = Resource(document = request.FILES['resourcefile'])
                document.author = Account.objects.filter(email=request.user.email).first()
                document.filename = request.POST['filename']
                document.save()
                return redirect('resource')
        else:
            form = ResourceForm()
    query=""
    if request.GET:
        query = request.GET.get('q','')
        context['query'] = str(query)
   
    resources = sorted(get_resource_queryset(query), key=attrgetter('date_published'), reverse= True)
    context['resources'] = resources
    return render(request, 'resource/resource_page.html', context)


# handles the deletion of document
def delete_document(request, pk):
        if request.method == 'POST':
            document = Resource.objects.get(pk=pk)
            document.delete()
        return redirect('resource')



      

