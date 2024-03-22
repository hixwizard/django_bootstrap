from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import DeleteView, UpdateView, ListView

from core.constants import POSTS_TO_DISPLAY
from .forms import CommentForm, PostForm, UserEditForm
from .models import Post
from .mixins import PostFormMixin, CommentMixin, CommonPostMixin
from .querysets import (
    get_annotated_posts, filter_published_posts, get_posts_in_category
)


class ProfileView(ListView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    paginate_by = POSTS_TO_DISPLAY
    author = None

    def get_author(self):
        if not self.author:
            self.author = get_object_or_404(
                User,
                username=self.kwargs['username']
            )
        return self.author

    def get_queryset(self):
        author = self.get_author()
        posts = get_annotated_posts(author)
        filtered_posts = filter_published_posts(
            posts, author, self.request.user
        )
        return filtered_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_author()
        return context


def index(request) -> HttpResponse:
    """Отображение главной страницы."""
    template = 'blog/index.html'

    page_obj = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related(
        'author',
        'location',
        'category'
    ).annotate(comment_count=Count('comments')).order_by(
        '-pub_date'
    )[:POSTS_TO_DISPLAY]
    context = {
        'page_obj': page_obj,
    }
    paginator = Paginator(page_obj, POSTS_TO_DISPLAY)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    return render(request, template, context)


def category_detail(request, slug) -> HttpResponse:
    """Отображение страницы с информацией о категории."""
    template = 'blog/category.html'

    posts, category = get_posts_in_category(slug)
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
    template_name = 'blog/create.html'
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user.username)
    return render(request, template_name, context={'form': form})


class EditPostView(PostFormMixin, LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs[self.pk_url_kwarg]}
        )


class DeletePostView(PostFormMixin, DeleteView):
    success_url = reverse_lazy('blog:index')


class ProfiletUpdateView(LoginRequiredMixin, UpdateView):
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
    comment = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        commentary = form.save(commit=False)
        commentary.author = request.user
        commentary.post = comment
        commentary.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    pass


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pass


class PostDeleteView(CommonPostMixin, LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserEditForm(instance=self.object)
        return context
