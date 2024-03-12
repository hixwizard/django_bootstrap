from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index'
    ),
    path(
        'registration/',
        views.YourRegistrationView.as_view(),
        name='registration'
    ),
    path(
        'category/<slug:slug>/',
        views.CategoryDetailView.as_view(),
        name='category_posts'
    ),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/create/',
        views.CreatePostView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:pk>/edit/',
        views.EditPostView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:pk>/delete/',
        views.DeletePostView.as_view(),
        name='delete_post'
    ),
    path(
        'posts/<int:post_id>/add_comment/',
        views.AddCommentView.as_view(),
        name='add_comment'
    ),
    path(
        'profile/<str:username>/',
        views.UserProfileView.as_view(),
        name='profile'
    ),
    path(
        'edit_profile/',
        views.edit_profile,
        name='edit_profile'
    ),
]
