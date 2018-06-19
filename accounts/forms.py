from django.contrib.auth import (
		authenticate,
		get_user_model
	)
from django import forms

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):

		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		user = authenticate(username=username, password=password)

		if not user:
			raise forms.ValidationError('This user does not exist.')
		if not user.check_password(password):
			raise forms.ValidationError('Incorrect Password')
		if not user.is_active:
			raise forms.ValidationError('This user is no longer active')

		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	first_name = forms.CharField(label='First Name')
	last_name = forms.CharField(label='Last Name')
	email = forms.EmailField(label='Email Address')
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'username',
			'email',
			'password',
			'password2'
		]

	def clean_password2(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		print(password, password2)
		if password != password2:
			raise forms.ValidationError('Passwords must match.')

		return password2

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError('This email has already been registered.')
		return email
