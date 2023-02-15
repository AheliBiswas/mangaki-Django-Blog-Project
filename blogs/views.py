from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Blog,Tag,Comment
from user.models import Profile
from .forms import CreateBlogForm,CommentForm,UpdateBlogForm
from django.db.models import Q
from .utils import searchQuery,commentBox,trendingblog,topslider_blogs_
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def home(request):
    search_item,blogs,tags = searchQuery(request)
    comment = Comment.objects.all()
    trending_blogs,profiles = trendingblog(request)
    topslider_blogs = topslider_blogs_(request)
    context = {'blogs':blogs,'tags':tags,'comment':comment,'search_item':search_item,'profiles':profiles,'trending_blogs':trending_blogs,'topslider_blogs':topslider_blogs}
    return render(request,'blogs/home.html',context)

def trendingblogs(request):
    page='trending_blog'
    blogs = Blog.objects.all()
    trending_blogs,profiles = trendingblog(request)
    context ={'page':page,'trending_blogs':trending_blogs,'profiles':profiles,'blogs':blogs}
    return render(request,'blogs/home.html',context)

def readBlog(request,pk):
    search_item,blogs,tags = searchQuery(request)
    blog = Blog.objects.get(id=pk)
    comments = commentBox(request,blog)
    userprofile = Profile.objects.get(username=blog.creator)
    trending_blogs,profiles = trendingblog(request)

    # comments = blog.comment_set.all()
    # if request.method == 'POST':
    #     Comment.objects.create(
    #         user = request.user,
    #         blog = blog,
    #         message = request.POST.get('comment')
    #     )
    #     return redirect('read-blog', pk=blog.id)

    context = {'blog':blog,'comments':comments,'userprofile':userprofile,'tags':tags,'search-item':search_item,'trending_blogs':trending_blogs}
    return render(request,'blogs/read-blog.html',context)

@login_required(login_url='login')
def updateComment(request,pk):
    page = "update"
    comment = Comment.objects.get(id=pk)
    form = CommentForm(instance=comment)
    if request.method == 'POST':
        form = CommentForm(request.POST,instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Message has been updated in "{comment.blog.title}" ')
            return redirect('read-blog',pk=comment.blog.id)
    context = {'form':form,'comment':comment,'page':page}
    return render(request,'blogs/update-delete-message.html',context)

@login_required(login_url='login')
def deleteComment(request,pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        comment.delete()
        messages.warning(request, f'Message has been deleted in "{comment.blog.title}" ')
        return redirect('read-blog',pk=comment.blog.id)
    context ={'comment':comment}
    return render(request,'blogs/update-delete-message.html',context)

@login_required(login_url='login')
def createBlog(request):
    form = CreateBlogForm()
    if request.method == 'POST':
        form = CreateBlogForm(request.POST,request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.creator = request.user
            form.save()
            messages.success(request, 'Blog has been uploaded ')
            return redirect('home')
    context = {'form':form}
    return render(request,'blogs/create-blog.html',context)

@login_required(login_url='login')
def updateBlog(request,pk):
    blog = Blog.objects.get(id=pk)
    form = UpdateBlogForm(instance=blog)
    if request.method == 'POST':
        form = UpdateBlogForm(request.POST,request.FILES,instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog has been updated ')
            return redirect('read-blog',pk=blog.id)
    context = {'form':form}
    return render(request,'blogs/update-blog.html',context)

@login_required(login_url='login')
def deleteBlog(request,pk):
    blog = Blog.objects.get(id=pk)
    blog.delete()
    messages.warning(request, 'Blog has been deleted successfully ')
    return redirect('home')


# Blogs By Genre:
def AnimeBlogs(request):
    topslider_blogs = topslider_blogs_(request)
    trending_blogs,profiles = trendingblog(request)
    anime_blogs = Blog.objects.filter(blog_genre='Anime')
    context = {'blogs':anime_blogs,'topslider_blogs':topslider_blogs,'trending_blogs':trending_blogs,'profiles':profiles}
    return render(request,'blogs/home.html',context)

def MangaBlogs(request):
    topslider_blogs = topslider_blogs_(request)
    trending_blogs,profiles = trendingblog(request)
    manga_blogs = Blog.objects.filter(blog_genre='Manga')
    context = {'blogs':manga_blogs,'topslider_blogs':topslider_blogs,'trending_blogs':trending_blogs,'profiles':profiles}
    return render(request,'blogs/home.html',context)

def WebtoonBlogs(request):
    topslider_blogs = topslider_blogs_(request)
    trending_blogs,profiles = trendingblog(request)
    webtoon_blogs = Blog.objects.filter(blog_genre='Webtoon')
    context = {'blogs':webtoon_blogs,'topslider_blogs':topslider_blogs,'trending_blogs':trending_blogs,'profiles':profiles}
    return render(request,'blogs/home.html',context)

def ManhwaBlogs(request):
    topslider_blogs = topslider_blogs_(request)
    trending_blogs,profiles = trendingblog(request)
    manhwa_blogs = Blog.objects.filter(blog_genre='Manhwa')
    context = {'blogs':manhwa_blogs,'topslider_blogs':topslider_blogs,'trending_blogs':trending_blogs,'profiles':profiles}
    return render(request,'blogs/home.html',context)

def ManhuaBlogs(request):
    topslider_blogs = topslider_blogs_(request)
    trending_blogs,profiles = trendingblog(request)
    manhua_blogs = Blog.objects.filter(blog_genre='Manhua')
    context = {'blogs':manhua_blogs,'topslider_blogs':topslider_blogs,'trending_blogs':trending_blogs,'profiles':profiles}
    return render(request,'blogs/home.html',context)