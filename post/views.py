from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.views.generic import ListView
from urllib import quote_plus

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Saved successfully")	
		return HttpResponseRedirect(instance.get_absolute_url())
	

	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

def post_detail(request, id=None):
	instance = get_object_or_404(Post, id = id)
	if instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	context = {
	"title" : instance.title,
	"instance" : instance,
	"share_string":share_string
    }
	return render(request, "post_detail.html", context)

def post_list(request):
	queryset_list = Post.objects.active()
	paginator = Paginator(queryset_list, 25) # Show 25 contacts per page.
	page_request_var = 'abc'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	
	context = {
	"object_list" : queryset,
	"title": "List",
	"page_request_var" : page_request_var
	}

	return render(request, "post_list.html", context)
    

def post_update(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id = id)
	form = PostForm(request.POST or None, request.FILES or None, instance= instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Updated")	
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title" : instance.title,
		"instance" : instance,
		"form": form,
	}
	return render(request, "post_form.html", context)


def post_delete(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise http404
	instance = get_object_or_404(Post, id = id)
	instance.delete()
	messages.success(request,"Successfully Deleted")	
	return redirect("post:list")
