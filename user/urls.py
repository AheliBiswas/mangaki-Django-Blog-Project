from django.urls import path
from user import views
urlpatterns = [
    path('about/',views.about,name='about'),
    
    path('blog-users/',views.Users,name='users'),
    path('user-profile/',views.userProfile,name='user-profile'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.userRegister,name='register'),
    path('verify/<token>/',views.verify,name='verify'),
    path('user-check/',views.userCheck,name='user-check'),
    path('forget-password/<token>/',views.forget_password,name='forget-password'),

    path('user-profile/update-profile/',views.updateUserProfile,name='update-profile'),
    path('user-profile/settings/<str:pk>/', views.userSettings,name='settings'),

    path('follow-unfollow/',views.follow_unfollow_account,name='follow-unfollow'),
    path('user-account/<str:pk>/',views.userAccount, name='user-account'),
    path('blogs-by/<str:pk>/', views.userBlogs,name='user-blogs'),
    path('delete-profile/<str:pk>/', views.deleteProfile, name='delete-profile'),
    path('contact/', views.contact, name='contact'),
]