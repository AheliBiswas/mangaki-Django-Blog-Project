from django.urls import path
from blogs import views
urlpatterns=[
    path('',views.home,name="home"),
    path('trending-blogs/',views.trendingblogs,name='trending-blog'),
    path('read-blog/<str:pk>/', views.readBlog, name='read-blog'),
    path('create-blog/', views.createBlog, name='create-blog'),
    path('update-blog/<str:pk>/', views.updateBlog, name='update-blog'),
    path('delete-blog/<str:pk>/', views.deleteBlog, name='delete-blog'),
    path('update_comment/<str:pk>/', views.updateComment,name='update-comment'),
    path('delete_comment/<str:pk>/', views.deleteComment,name='delete-comment'),
    
    path('animeblogs/',views.AnimeBlogs,name='anime-blog'),
    path('mangablogs/',views.MangaBlogs,name='manga-blog'),
    path('webtoonblogs/',views.WebtoonBlogs,name='webtoon-blog'),
    path('manhwablogs/',views.ManhwaBlogs,name='manhwa-blog'),
    path('manhuablogs/',views.ManhuaBlogs,name='manhua-blog'),
]