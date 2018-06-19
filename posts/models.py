from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe

from markdown_deux import markdown

from comments.models import Comment
from .utils import get_read_time
# Create your models here.


class PostManager(models.Manager):

	def active(self,*args,**kwargs):
		return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())


class Post(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	title 			= models.CharField(max_length = 256)
	image 			= models.ImageField(null=True, blank=True, width_field='width_field', height_field='height_field')
	slug 			= models.SlugField(unique=True)
	height_field 	= models.IntegerField(default=0)
	width_field 	= models.IntegerField(default=0)
	content 		= models.TextField()
	draft 			= models.BooleanField(default=False)
	publish 		= models.DateField(auto_now=False, auto_now_add=False)
	read_time		= models.IntegerField(null=True, blank=True)
	created_on 		= models.DateTimeField(auto_now_add = True)
	updated_on 		= models.DateTimeField(auto_now = True)

	objects = PostManager()

	class Meta:
		ordering = ['-created_on', '-updated_on']
		
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('posts:detail', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('posts:delete', kwargs={'slug':self.slug})

	def get_edit_url(self):
		return reverse('posts:update', kwargs={'slug':self.slug})

	def get_markdown(self):
		return mark_safe(markdown(self.content))

	@property	
	def comments(self):
		return Comment.objects.filter_by_instance(self)

	@property
	def get_content_type(self):
		return ContentType.objects.get_for_model(self.__class__)


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug

	qs = Post.objects.filter(slug=slug).order_by('-id')

	if qs.exists():
		new_slug = "%s-%s" %(slug,qs.first().id)
		return create_slug(instance, new_slug)
	return slug



def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug or Post.objects.filter(slug=instance.slug).exists():
		instance.slug = create_slug(instance)

	if instance.content:
		html_string = instance.get_markdown()
		read_time = get_read_time(html_string)
		instance.read_time = read_time


pre_save.connect(pre_save_post_receiver, sender=Post)