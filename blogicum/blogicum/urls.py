from django.conf import settings
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.conf.urls.static import static
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
    path(
        'auth/password_change/',
        views.PasswordChangeView.as_view(),
        name='password_change'
    ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        path('__debug__/', include(debug_toolbar.urls)),
    )
