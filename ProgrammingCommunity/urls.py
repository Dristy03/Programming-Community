"""ProgrammingCommunity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from account.views import registration_view, welcome_view, home_view, login_view, logout_view,activate
from resource.views import resource_view,delete_document
from user_profile.views import profile_view
from menu.views import menu_view, menu_stdlist_view, menu_tchlist_view, about_view
from post.views import PostNotificationView,PostDetailsView,mark_all_notification
from contact_us.views import contactusview
from contests.views import contest_view


# All the url paths of the website
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_view, name='welcome'),
    path('register/', registration_view, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'), 
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('post/', include('post.urls', 'post')),
    path('post/<int:pk>',PostDetailsView.as_view(),name='post_details'),
    path('resource/', resource_view, name='resource'),
    path('resource/<int:pk>',delete_document, name='delete_document' ),
    path('profile/', profile_view, name='profile'),
    path('menu/', menu_view, name ='menu_default'),
    path('menu/menu_stdlist', menu_stdlist_view, name ='menu_stdlist'),
    path('menu/menu_tchlist', menu_tchlist_view, name ='menu_tchlist'),
    path('menu/about', about_view, name ='about'),
    path('contact_us/contact_us', contactusview, name = 'contact_us'),
    path('contests/',contest_view,name='contests'),
    path('notifications/<int:notification_pk>/post/<int:post_pk>',PostNotificationView.as_view(),name='post_notification'),
    path('mark_all/',mark_all_notification.as_view(),name='mark_all'),

]

# paths for storing the static and media files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)