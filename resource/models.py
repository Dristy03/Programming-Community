from django.db import models
from django.conf import settings
from django.db.models.query_utils import Q

# sets directory path for the resource uploaded
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'documents/{0}/{1}'.format(instance.author.email, filename)

# resource model
class Resource(models.Model):
	filename = models.CharField(max_length=30, null=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	document = models.FileField(upload_to=user_directory_path,blank=True,null=True)
	date_published = models.DateTimeField(auto_now_add=True)


	def __str__(self) -> str:
		return f'{self.author.email}-{self.document}'

	def delete(self, *args, **kwargs):
		self.document.delete()
		super().delete(*args, **kwargs)

# filters resources by search query

def get_resource_queryset(query=None):
	queryset  = []
	queries= query.split(" ")
	for q in queries:
		resources = Resource.objects.filter(
				Q(filename__icontains=q)
			).distinct()

		for resource in resources:
			queryset.append(resource)
	return list(set(queryset))
