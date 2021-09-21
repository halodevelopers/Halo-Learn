from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
# Using a custom model Manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

# Post Model
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=250, blank=False, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='blog_post')
    image = models.ImageField(upload_to='featured_image/%Y/%m/%d/', null=True, blank=False) #this
    # body = models.TextField()
    body=RichTextUploadingField(null=True, blank=False) # add this
    
    
    
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    tags = TaggableManager() 
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title
    
    
    # defining our cutom model manager for use in our view
    objects = models.Manager() # default manager
    published = PublishedManager() # custom manager
    
    
    # conical url patterns
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])
    
    
    # added after get_absolute_url function
    # to get comment with parent is none and active is true, we can use this in template
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

# comment model    
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.SET_NULL, null=True, blank=True,related_name="comments")
    name=models.CharField(max_length=50, null=True, blank=True)
    email=models.EmailField()
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    body = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)