from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import operator
from django.db.models import Q

# Create your views here.
def index(request,page):
	# get(country="United States")
	query = request.GET.get('q')
	if (query==None):
		query=""
	profiles = UserProfile.objects.filter(Q(description__icontains=query))
	paginator = Paginator(profiles, 54) 

	try:
		contacts=paginator.page(page)
	except PageNotAnInteger:
		contacts=paginator.page(1)
	except EmptyPage:
		contacts=paginator.page(paginator.num_pages)


	context={ 
		'user_profiles' : contacts,
		'page': page,
		}
	return render(request, 'pals/index.html' , context)

def delete_user(request, userId):
	x = UserProfile.objects.get(pk=userId)
	x.delete()
	return  HttpResponseRedirect(reverse('pals:index', kwargs={'page':1}))

def detail(request, userId,page):
	x = UserProfile.objects.get(pk=userId)
	context = {
		'userProfile':x,
		'page':page,
	}
	return render(request, 'pals/detail.html', context)