from django.shortcuts import redirect


def post_redirect_view(request):
	return redirect('/posts')