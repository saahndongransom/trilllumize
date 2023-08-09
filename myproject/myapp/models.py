from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(unique=True, populate_from='title', editable=False)
    content = RichTextField()
    author = models.CharField(max_length=100)
    pub_date = models.DateField(default=timezone.now)
    image_url = models.URLField()
    categories = models.ManyToManyField('myapp.Category')
    tags = models.ManyToManyField('myapp.Tag')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name




class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.blog_post.title}"

class SubscribedUsers(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Resource(models.Model):
    RESOURCE_TYPES = (
        ('ebook', 'E-Book'),
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('article', 'Article'),
        ('picture', 'Picture'),
        ('software', 'Software'),
        ('tutorial', 'Tutorial'),
        ('audio', 'Audio'),
        # Add other resource types here
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # Add other fields if necessary

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)




