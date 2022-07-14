from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from blog.models import Post, Comment
from blog.forms import CommentForm

def blog(request, **kwargs):
    posts = Post.objects.filter(status = 1)

    if kwargs.get('category_name') != None:
        posts = posts.filter(category__name = kwargs['category_name'])

    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username = kwargs['author_username'])

    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])

    posts = Paginator(posts, 3)
    try:
        pageNumber = request.GET.get('page')
        posts = posts.get_page(pageNumber)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)

    context = {'posts': posts}

    return render(request, 'blog/blog-home.html', context)

def blog_single(request, pid):
    if request.method == 'POST' :
        form = CommentForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment is submitted successfully.')
        else :
            messages.add_message(request, messages.ERROR, 'Submitting of your comment failed!')

    publishedPosts = Post.objects.filter(status = 1)
    post = get_object_or_404(publishedPosts, pk = pid)

    if not post.login_required:
        prevPost = getPreviousPost(publishedPosts, pid)
        nextPost = getNextPost(publishedPosts, pid)
        comments = Comment.objects.filter(post = post.id, approved = True)

        incrementPostViewCount(post)

        form = CommentForm()

        context = {'post': post, 'prev_post': prevPost, 'next_post': nextPost, 'comments': comments, 'form': form}

        return render(request, 'blog/blog-single.html', context)
    else:
        return HttpResponseRedirect(reverse('accounts:login'))

def blog_search(request):
    posts = Post.objects.filter(status = 1)

    if request.method == 'GET':
        if query := request.GET.get('query') :
            posts = posts.filter(content__contains = query)

    context = {'posts': posts}

    return render(request, 'blog/blog-home.html', context)

def incrementPostViewCount(post):
    post.views_count += 1
    post.save()

def getPreviousPost(posts, pid):
    return posts.filter(id__lt = pid).order_by('id').last()

def getNextPost(posts, pid):
    return posts.filter(id__gt = pid).order_by('id').first()
