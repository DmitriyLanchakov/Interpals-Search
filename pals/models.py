from django.db import models

# Create your models here.
class UserProfile(models.Model):
	username = models.CharField(max_length=50)
	city = models.CharField(max_length=50,default='none')
	state = models.CharField(max_length=50,default='none')
	country = models.CharField(max_length=50,default='none')
	age = models.IntegerField(default=0)
	imageUrl = models.URLField(max_length=500, default='none')
	description = models.TextField(max_length=5000, default='none')
	# languages = models.ArrayField(models.ArrayField(models.IntegerField()))

	def __str__(self):
		return self.username+" "+self.country