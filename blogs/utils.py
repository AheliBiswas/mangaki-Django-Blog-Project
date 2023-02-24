from .models import Blog,Tag,Comment
from user.models import Profile
from django.db.models import Q
from django.shortcuts import render,redirect
from django.contrib import messages

def searchQuery(request):
    search_item = ''
    if request.GET.get('search_item'):
        search_item = request.GET.get('search_item')

    tags = Tag.objects.filter(name__icontains=search_item)

    blogs = Blog.objects.distinct().filter(
        Q(title__icontains=search_item) |
        Q(tag__in = tags) |
        Q(blog_genre__iexact=search_item) |
        Q(creator__username__contains=search_item)
        ).order_by('-created')
    # blogs = Blog.objects.all().order_by('-created')

    return search_item,blogs,tags

def commentBox(request,blog):
    comments = blog.comment_set.all()
    if request.method == 'POST':
        message = Comment.objects.create(
            user = request.user,
            blog = blog,
            message = request.POST.get('comment')
        )
        message.save()
        messages.success(request, 'You have commented successfully ')
        # return redirect('read-blog', pk=blog.id)

    return comments

def trendingblog(request):
    profiles = Profile.objects.all().order_by('-created')[0:4]
    blogs = Blog.objects.all()
    trending_blogs =[]
    for blog in blogs:
        if blog.comment_set.count() >= 5:
            trending_blogs.append(blog)
    return trending_blogs,profiles

def topslider_blogs_(request):
    blogs = Blog.objects.all()
    topslider_blogs =[]
    for blog in blogs:
        if blog.comment_set.count() >=1:
           topslider_blogs.append(blog) 

    return topslider_blogs