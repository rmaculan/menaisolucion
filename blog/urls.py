from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.read_blog_posts, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('edit_profile/edit', views.edit_profile, name='edit_profile'),
    path('delete_profile/<str:username>', views.delete_profile, name='delete_profile'),
    path('my_posts/', views.read_my_posts, name='my_posts'),
    path('<uuid:post_id>/', views.read_blog_post, name='post_detail'),
    path('create_blog_post/', views.create_blog_post, name='create_blog_post'),
    path('delete/<uuid:post_id>/', views.delete_blog_post, name='delete_blog_post'),
    path('<uuid:post_id>/like/', views.like_post, name='like_post'),
    path('<uuid:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('<uuid:post_id>/comment/', views.create_comment, name='create_comment'),
    path('<uuid:post_id>/<int:comment_id>/edit/', views.update_comment, name='update_comment'),
    path('<uuid:post_id>/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    
]