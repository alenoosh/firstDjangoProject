from django import template
from blog.models import Post

register = template.Library()

@register.inclusion_tag('main/recent-blog-area.html')
def recentblogarea():
    posts = Post.objects.filter(status = 1)[:6]

    return { 'posts': posts }
