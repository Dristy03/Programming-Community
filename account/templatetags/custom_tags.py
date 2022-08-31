from django import template
from post.models import Post,Comment,Notification


register = template.Library()

@register.inclusion_tag('post/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    unseen = Notification.objects.filter(to_user= request_user,user_has_seen = False)
    notifications = Notification.objects.filter(to_user= request_user).order_by('user_has_seen','-date')
    unread_count = unseen.count()
    return {'notifications': notifications,'unread_count':unread_count}