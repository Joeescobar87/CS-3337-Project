from django.contrib import admin
from django.urls import path
from django.urls import include
# edit
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic import TemplateView
from bookMng.views import Register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/success', TemplateView.as_view(
        template_name='registration/register_success.html'),
        name='register-success'),
    path('', include('django.contrib.auth.urls')),
    path('', include('bookMng.urls')),
    path('register/', Register.as_view(), name='register'),
    # edit
    path('', include('cart.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
