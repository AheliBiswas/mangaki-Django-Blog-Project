from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from .models import Profile
from .forms import RegisterUserCreationForm,UpdateProfileForm
from blogs.models import Blog,Tag,Comment
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.core.mail import send_mail



# Create your views here.

def about(request):
    return render(request,'user/about.html')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Profile.objects.get(username=username)
        try:
            if user.is_verified == False:
                messages.error(request,'your email has not been veryfied')
            else:
                 user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request,password=password,username=username)
        if user is not None:
            login(request,user)
            messages.success(request, 'You have logged in successfully')
            return redirect('home')
        else:
            messages.error(request,'password is wrong')
            

    return render(request,'user/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def userRegister(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    form = RegisterUserCreationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            if User.objects.filter(username=username).first():
                messages.error(request,'username is already taken')
                return redirect('register')

            if User.objects.filter(email=email).first():
                messages.error(request,'email is already taken')
                return redirect('register')

            user = User.objects.create(
                username = request.POST.get('username'),
                email = request.POST.get('email')
            )
            user.set_password(request.POST.get('pass'))
            user.save()
            token = str(user.profile.id)
            registrationConfMail(email,token)

        except Exception as e:
            print(e)

        messages.success(request, 'We have send you a mail for account verification')
        

    context = {}
    return render(request,'user/register.html',context)

#veryfiying email after registering the profile
def verify(request,token):
    profile = Profile.objects.get(id=token)
    if profile:
        profile.is_verified = True
        profile.save()
        messages.success(request, 'Your email has been verified')
        return redirect('login')

def userCheck(request):
    recover_text = request.POST.get('text')
    if recover_text:
        recover_email = Profile.objects.filter(email=recover_text).first()
        recover_name = Profile.objects.filter(username=recover_text).first()
    try:
        if recover_email is not None:
            email = recover_email.email
            token = recover_email.id
            passwordConfMail(email,token)
            messages.success(request, 'Verification mail has been send to you')
        elif recover_name == Profile.objects.get(username=recover_name):
            token = recover_name.id
            email = recover_name.email
            passwordConfMail(email,token)
            messages.success(request, 'Verification mail has been send to you')

    except Exception as e:
        print(e)
    return render(request,'user/email_check.html')


#sending email after registering
def registrationConfMail(email, token):
    subject = 'Your account need to be verified'
    message = f'Hi click the link to verify your account http://127.0.0.1:8000/user/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

#sending email for forget password after user verification
def passwordConfMail(email, token):
    subject = 'You have requested for Password Recovery'
    message = f'Hi click this link to change your password http://127.0.0.1:8000/user/forget-password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def forget_password(request,token):
    user = Profile.objects.get(id=token)
    if request.method == 'POST':
        password = request.POST.get('pass')
        if password:
            user.user.set_password(password)
            user.user.save()
            messages.success(request,'Your password has succefully changed')
            return redirect('login')
    return render(request,'user/forget_password.html')


@login_required(login_url='login')
def follow_unfollow_account(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        pk = request.POST.get('pk')
        my_profile = Profile.objects.get(user=request.user)
        follow_account = Profile.objects.get(id=pk)
        if follow_account.user in my_profile.following.all():
            my_profile.following.remove(follow_account.user)
            messages.info(request, f'You have unfollowed "@{follow_account.user.username}" ')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            my_profile.following.add(follow_account.user)
            messages.info(request, f'You have followed "@{follow_account.user.username}" ')
            return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def Users(request):
    
    #filtering out users that I follow
    logged_in_user = request.user.profile
    followings = logged_in_user.following.all()
    list = []
    for x in followings:
        p = Profile.objects.get(username=x)
        list.append(p)
    #appending them in a list 

    search_user = ''
    if request.GET.get('search_user'):
        search_user = request.GET.get('search_user')

    profiles = Profile.objects.filter(
            Q(name__icontains=search_user)|
            Q(username__icontains=search_user)
        ).exclude(user=request.user)

    #as the view is only executing after loading the whole page
    # so we need to send a whole list of users that does not follow our
    # logged in user. So that profiles can be loaded with the whole page.
    profiles1 = []
    my_profile = Profile.objects.get(user=request.user)
    for profile in profiles:
        if profile.user not in my_profile.following.all():
            profiles1.append(profile)
    print(profiles1)
    #this is sending the profile infos that are not in the user following
    #section and sending them into the context as a list 

    context = {'profiles':profiles,'search_user':search_user, 'followings':list,'profiles1':profiles1}
    return render(request,'user/users.html',context)

@login_required(login_url='login')
def userAccount(request,pk):
    userprofile = Profile.objects.get(id=pk)

    # this getting the followers of a profile by checking if the profile exists in any other tables.
    followers = len(Profile.objects.filter(following = userprofile.user.id))

    # this is getting the User by matching the username's of the Profile model and User model
    user = User.objects.get(username=userprofile)

    # this is filtering out the blogs belong to that user name
    userblogs = user.blog_set.all().order_by('-created')
    my_profile = Profile.objects.get(user=request.user)
    follow_account = Profile.objects.get(id=pk)
    if follow_account.user in my_profile.following.all():
        follow = True
    else:
        follow = False
    context = {'userprofile':userprofile,'userblogs':userblogs,'follow':follow,'followers':followers}
    return render(request,'user/user-profile.html',context)

def userBlogs(request,pk):
    userprofile = Profile.objects.get(id=pk)
    
    user = User.objects.get(username=userprofile)
    userblogs = user.blog_set.all().order_by('-created')

    context = {'userprofile':userprofile,'userblogs':userblogs}
    return render(request,'user/user-related-blogs.html',context)

def userProfile(request):
    # this is getting the Profile of the logged in user by it's UUID
    # Profile.objects.get(id=pk)(do not use this)
    userprofile = request.user.profile
    followers = len(Profile.objects.filter(following = userprofile.user.id))
    # this is getting the User by matching the username's of the Profile model and User model
    user = User.objects.get(username=userprofile)

    # this is filtering out the blogs belong to that user name
    userblogs = user.blog_set.all().order_by('-created')
    context = {'userprofile':userprofile,'userblogs':userblogs,'followers':followers}
    return render(request,'user/user-profile.html',context)

@login_required(login_url='login')
def updateUserProfile(request):
    userprofile = request.user.profile
    user = User.objects.get(username=userprofile)
    userblogs = user.blog_set.all().order_by('-created')
    followers = len(Profile.objects.filter(following = userprofile.user.id))
    form = UpdateProfileForm(instance=request.user.profile)

    # if request.method == 'POST':
    #     form = UpdateProfileForm(request.POST,request.FILES,instance=request.user.profile)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('user-profile')
    
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST,request.FILES,instance=request.user.profile)
        userprofile.name = request.POST.get('name')
        userprofile.username = request.POST.get('username')
        userprofile.email = request.POST.get('email')
        userprofile.bio = request.POST.get('bio')
        userprofile.social_instagram = request.POST.get('social_instagram')
        userprofile.social_twitter = request.POST.get('social_twitter')
        userprofile.social_youtube = request.POST.get('social_youtube')

        if form.is_valid():
            form.save()

        userprofile.save()
        messages.success(request, 'Profile has successfully updated!')
        return redirect('user-profile')
        pass

    context = {'form':form,'userprofile':userprofile,'userblogs':userblogs,'followers':followers}
    return render(request,'user/update-user-profile.html',context)

@login_required(login_url='login')
def deleteProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    profile.delete()
    messages.info(request, 'Profile has successfully deleted!')
    return redirect('home')

@login_required(login_url='login')
def userSettings(request,pk):
    userprofile = Profile.objects.get(id=pk)
    context ={'userprofile':userprofile}
    return render(request,'user/settings.html',context)

def contact(request):
    context = {}
    return render(request,'user/contact.html',context)