from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.timezone import now
from django.views.generic import DeleteView, UpdateView, ListView

from .constants import POSTS_TO_DISPLAY
from .forms import CommentForm, PostForm, UserEditForm
from .models import Category, Comment, Post


class ProfileView(ListView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    paginate_by = POSTS_TO_DISPLAY

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        posts = author.posts.annotate(
            comment_count=Count('comments')
        ).order_by(
            '-pub_date').select_related('category', 'author', 'location')
        if author != self.request.user:
            posts = posts.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=now()
            )
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
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

    return render(request, template, context)


def category_detail(request, slug) -> HttpResponse:
    """Отображение страницы с информацией о категории."""
    template = 'blog/category.html'

    category = get_object_or_404(Category, slug=slug, is_published=True)

    post_list = Post.objects.filter(
        category=category,
        pub_date__lte=timezone.now(),
        is_published=True
    ).select_related(
        'author',
        'location',
        'category',
    ).order_by('-pub_date')

    paginator = Paginator(post_list, POSTS_TO_DISPLAY)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    comment_form = CommentForm()

    context = {
        'category': category,
        'page_obj': posts,
        'comment_form': comment_form,
    }

    return render(request, template, context)


def post_detail(request, post_id) -> HttpResponse:
    """Отображение подробной информации о посте."""
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            pk=post_id
        ).select_related(
            'author',
            'location',
            'category'
        )
    )

    if not request.user.is_authenticated:
        raise Http404("Страница поста недоступна.")

    if request.user == post.author:
        pass
    elif not post.is_published:
        raise Http404("Страница поста недоступна.")
    elif post.pub_date > timezone.now():
        if request.user != post.author:
            raise Http404("Страница поста недоступна.")

    context = {
        'post': post,
        'form': CommentForm(),
        'comments': post.comments.select_related('author'),
    }

    return render(request, template, context)


@login_required
def post_create(request) -> HttpResponse:
    template_name = 'blog/create.html'
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user.username)
    return render(request, template_name, context={'form': form})


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(settings.URL_LOGIN))
        elif post.author != request.user:
            return HttpResponseRedirect(
                reverse('blog:post_detail', kwargs={'post_id': post.id})
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs[self.pk_url_kwarg]}
        )


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('post_id'))
        if post.author != request.user:
            return redirect('blog:post_detail', self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)

    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm


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


class CommentMixin:
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    comment = None

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Comment, pk=kwargs.get(
                'comment_id',
                'post_id'
            )
        )
        if instance.author != request.user:
            return redirect('blog:post_detail', self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.comment = self.comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.kwargs.get('post_id')})


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    pass


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pass


class CommonPostMixin:
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    form_class = UserEditForm
    posts = None

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('post_id'))
        if post.author != request.user:
            return redirect('blog:post_detail', self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(CommonPostMixin, LoginRequiredMixin, UpdateView):

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.object.pk})


class PostDeleteView(CommonPostMixin, LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserEditForm(instance=self.object)
        return context
