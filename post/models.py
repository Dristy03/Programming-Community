from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse
from random import randint
from django.utils import timezone
from django.db.models.query_utils import Q


# upload location of post image
def upload_location(instance, filename):
	file_path = 'post/{author_id}/{filename}'.format(
				author_id=str(instance.author.id), filename=filename)
	return file_path

# post modal
class Post(models.Model):
	text 					= CKEditor5Field('text',max_length=5000, null=False, blank=False, config_name='extends')
	date_published 			= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated 			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug 					= models.SlugField(blank=True, unique=True)
	image 					= models.ImageField(blank=True,null=True)

	def __str__(self):
		return self.text

@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		extra = str(randint(1, 1000000))
		instance.slug = slugify(instance.author.email + "-" + extra)

pre_save.connect(pre_save_blog_post_receiver, sender=Post)


# comment upload location
def comment_upload_location(instance, filename):
    file_path = 'comments/{author_id}/comment_pic_{filename}'.format(
        author_id=str(instance.pk), filename=filename)
    return file_path

# comment model
class Comment(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="comment_author")
	post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="comments")
	body = models.TextField(null=False)
	date_published = models.DateTimeField(auto_now_add=True)
	comment_image = models.ImageField(upload_to=comment_upload_location,null = True,blank = True)
	def __str__(self):
		return f'{self.post.slug}-- comment {self.body}'

	def get_absolute_url(self):
		return reverse("home_view", kwargs={"pk": self.pk})
	
# notification model
class Notification(models.Model):
	# 1 = post 2 = comment
	notification_type = models.IntegerField()
	to_user = 	models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="notification_to",null=True)
	from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="notification_from",null=True)
	post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True,related_name='+')
	date = models.DateTimeField(default = timezone.now)
	user_has_seen = models.BooleanField(default=False)

# filters post search wise
def get_post_queryset(query=None):
	queryset  = []
	queries= query.split(" ")
	for q in queries:
		posts = Post.objects.filter(
			Q(text__icontains=q)
		).distinct()

		for post in posts:
			queryset.append(post)
	return list(set(queryset))

