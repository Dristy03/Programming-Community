from django.urls import path,reverse
from post.views import (
	create_post_view,
    add_comment_view,
    PostNotificationView,
    PostDetailsView,
    delete_post_view,
    edit_post_view
)

app_name = 'post'

# sets the urls of the subsections under the post app

urlpatterns = [
    path('create/', create_post_view, name="create"),
    path('comment/<int:pk>',add_comment_view, name="comment"),
    path('delete/<int:pk>',delete_post_view, name="delete"),
    path('edit/<int:pk>',edit_post_view, name="edit"),
  
 ]