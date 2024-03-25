from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/',
         views.category_detail, name='category_posts'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create/', views.post_create, name='create_post'),
    path(
        'posts/<int:post_id>/edit/',
        views.EditPostView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.DeletePostView.as_view(),
        name='delete_post'
    ),
    path(
        'profile/<slug:username>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'profile_edit/', views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path('posts/<post_id>/comment/', views.add_comment, name='add_comment'),
    path('posts/<post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path(
        'posts/<post_id>/delete_comment/<int:comment_id>/',
        views.CommentDeleteView.as_view(), name='delete_comment'
    ),
]
