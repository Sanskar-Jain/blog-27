from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import PermissionDenied

from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404

from comments.models import Comment
from comments.forms import CommentForm
from .models import Post
from .forms import PostForm
from .utils import get_read_time

import urllib
# Create your views here.

def post_list(request):
	if not request.user.is_staff or not request.user.is_superuser:
		queryset_list = Post.objects.active()
	else:
		queryset_list = Post.objects.all()

	query = request.GET.get('q')
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset_list, 6)
	page = request.GET.get('page')
	try:
		queryset = paginator.get_page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		'objects': queryset,
		'title': 'List'
	}
	return render(request, 'post_list.html', context)


def post_detail(request,slug=None):
	instance = get_object_or_404(Post,slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		print(instance.draft)
		print(timezone.now().date())
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	initial_data = {
		'content_type': instance.get_content_type,
		'object_id': instance.id
	}

	comments = instance.comments
	comment_form = CommentForm(request.POST or None, initial=initial_data)

	if request.POST:
		if not request.user.is_authenticated:
			return redirect('/login/?next={slug}'.format(slug=slug))
		if comment_form.is_valid():
			c_type = comment_form.cleaned_data.get("content_type")
			content_type = ContentType.objects.get(model=c_type)
			object_id = comment_form.cleaned_data.get("object_id")
			content = comment_form.cleaned_data.get("content")
			parent_obj = None

			try:
				parent_id = int(request.POST.get('parent_id'))
			except:
				parent_id = None

			if parent_id:
				parent_qs = Comment.objects.filter(id=parent_id)
				if parent_qs.exists():
					parent_obj = parent_qs.first()


			new_comment, created = Comment.objects.get_or_create(
								user=request.user,
								content_type=content_type,
								object_id=object_id,
								content=content,
								parent=parent_obj,
							)
			return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	context = {
		'title': instance.title,
		'instance': instance,
		'comments': comments,
		'comment_form': comment_form, 
	}
	return render(request, 'post_detail.html', context)


def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise PermissionDenied
	form = PostForm(request.POST or None, request.FILES or None)
	if request.POST:
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, 'Successfully Created.')
			return HttpResponseRedirect(instance.get_absolute_url())
		else:
			messages.error(request, 'Not Successfully Created.')
	context = {
		'title': 'New Post',
		'form': form,

	}
	return render(request, 'post_form.html', context)


def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise PermissionDenied
	instance = get_object_or_404(Post,slug=slug)
	if request.user != instance.user:
		raise PermissionDenied
	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, 'Saved.')
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		'title': 'New Post',
		'form': form,

	}
	context = {
		'title': instance.title,
		'instance': instance,
		'form': form
	}
	return render(request, 'post_form.html', context)


def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise PermissionDenied
	instance = get_object_or_404(Post, slug=slug)
	if request.user != instance.user:
		raise PermissionDenied

	if request.method == 'POST':
		instance.delete()
		messages.success(request,'Post Deleted.')
		return HttpResponseRedirect('/posts/')

	context = {
		'obj': instance
	}
	return render(request, 'post_delete.html', context)