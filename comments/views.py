from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.conf import settings

from .models import Comment
from .forms import CommentForm
# Create your views here.

LOGIN_URL = settings.LOGIN_URL


def comment_thread(request, id=None):
	try:
		obj = Comment.objects.get(id=id)
	except:
		raise Http404
	
	initial_data = {
		'content_type': obj.content_type,
		'object_id': obj.object_id
	}

	form = CommentForm(request.POST or None, initial=initial_data)

	if request.POST:
		if not request.user.is_authenticated:
			return redirect('/login/?next=/comments/{id}'.format(id=id))
		if form.is_valid():
			c_type = form.cleaned_data.get("content_type")
			content_type = ContentType.objects.get(model=c_type)
			object_id = form.cleaned_data.get("object_id")
			content = form.cleaned_data.get("content")
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
			return HttpResponseRedirect(new_comment.parent.get_absolute_url())

	context = {
		'comment': obj,
		'form': form,
	}
	return render(request, 'comment_thread.html', context)

@login_required
def comment_delete(request, id=None):
	try:
		obj = Comment.objects.get(id=id)
	except:
		raise Http404

	if obj.user != request.user:
		raise PermissionDenied

	if request.method == 'POST':
		if not obj.is_parent:
			parent_obj_url = obj.parent.get_absolute_url()
		else:
			parent_obj_url = obj.content_object.get_absolute_url()
		obj.delete()
		messages.success(request,'Comment Deleted.')
		return HttpResponseRedirect(parent_obj_url)

	context = {
		'comment': obj,
	}
	return render(request, 'comment_delete.html', context)