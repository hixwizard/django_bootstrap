from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import CommentForm, PostForm
from .models import Post, Comment


class PostFormMixin:
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    form_class = PostForm
    posts = None

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('post_id'))
        if post.author != request.user:
            return redirect('blog:post_detail', self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)


class CommonPostMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            self.model, pk=kwargs.get(self.pk_url_kwarg)
        )
        if instance.author != request.user:
            return redirect('blog:post_detail', post_id=instance.pk)
        return super().dispatch(request, *args, **kwargs)


class CommentMixin(CommonPostMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    comment = None

    def dispatch(self, request, *args, **kwargs):
        comment_id = kwargs.get(self.pk_url_kwarg)
        self.comment = get_object_or_404(self.model, pk=comment_id)
        if self.comment.author != request.user:
            return redirect('blog:post_detail', post_id=self.comment.post.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.comment = self.comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs.get('post_id')}
        )
