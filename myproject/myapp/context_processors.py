# context_processors.py
from .models import BlogPost

def posts_context(request):
    posts = BlogPost.objects.all()
    return {'posts': posts}
