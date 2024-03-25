from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import DeleteView, UpdateView, ListView

from core.constants import POSTS_TO_DISPLAY
from .forms import CommentForm, PostForm, UserEditForm
from .models import Post, Category
from .mixins import PostFormMixin, CommentMixin
from .pagitane import paginate
from .querysets import filter_posts


class ProfileView(ListView):
    """Отображение страницы профиля."""

    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    paginate_by = POSTS_TO_DISPLAY
    author = None

    def get_author(self):
        if not self.author:
            self.author = get_object_or_404(
                User, username=self.kwargs['username']
            )
        return self.author

    def get_queryset(self):
        author = self.get_author()
        posts = author.posts.all().order_by('-pub_date')
        if author != self.request.user:
            posts = filter_posts(posts)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_author()
        return context


def index(request) -> HttpResponse:
    """Отображение главной страницы."""
    template = 'blog/index.html'
    post_list = filter_posts(Post.objects.all(), published_only=True)
    page_obj = paginate(post_list, request, POSTS_TO_DISPLAY)
    context = {
        'page_obj': page_obj,
    }

    return render(request, template, context)


def category_detail(request, slug) -> HttpResponse:
    """Отображение страницы с информацией о категории."""
    template = 'blog/category.html'

    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = filter_posts(
        Post.objects.all(), category_slug=slug, published_only=True
    )
    posts = paginate(post_list, request, POSTS_TO_DISPLAY)
    comment_form = CommentForm()

    context = {
        'category': category,
        'page_obj': posts,
        'comment_form': comment_form,
    }

    return render(request, template, context)


@login_required
def post_detail(request, post_id) -> HttpResponse:
    """Отображение подробной информации о посте."""
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            Q(pk=post_id),
            (Q(is_published=True, pub_date__lte=timezone.now())
             | Q(author=request.user))
        ).select_related(
            'author',
            'location',
            'category'
        )
    )

    context = {
        'post': post,
        'form': CommentForm(),
        'comments': post.comments.select_related('author'),
    }

    return render(request, template, context)


@login_required
def post_create(request):
    """Отображение страницы создания профиля."""
    template_name = 'blog/create.html'
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user.username)
    return render(request, template_name, context={'form': form})


class EditPostView(PostFormMixin, LoginRequiredMixin, UpdateView):
    """Отображение страницы редактирования поста."""

    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs[self.pk_url_kwarg]}
        )


class DeletePostView(PostFormMixin, DeleteView):
    """Отображение страницы удаления профиля."""

    success_url = reverse_lazy('blog:index')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Отображение страницы редактирования профиля."""

    form_class = UserEditForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})


@login_required
def add_comment(request, post_id) -> HttpResponse:
    """Отображение страницы комметария."""
    comment = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        commentary = form.save(commit=False)
        commentary.author = request.user
        commentary.post = comment
        commentary.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    """Отображение страницы редактирования комметария."""

    pass


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    """Отображение страницы удаления комметария."""

    pass


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Отображение страницы удаления поста."""

    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            self.model, pk=kwargs.get(self.pk_url_kwarg)
        )
        if instance.author != request.user:
            return redirect('blog:post_detail', post_id=instance.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserEditForm(instance=self.object)
        return context
