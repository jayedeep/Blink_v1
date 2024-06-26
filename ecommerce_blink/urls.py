"""ecommerce_blink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import users
import products
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',include('users.urls')),
    path('accounts/', include('allauth.urls')),
    
    path('',include('products.urls')),
    path('admin/',include('staffs.urls')),
    path('admin/',include('notifications_app.urls')),

    # path('social-auth/', include('social_django.urls', namespace="social")),

    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'users.views.page_not_found'  # Replace with your app's custom 500 view
handler500 = 'users.views.server_error'  # Replace with your app's custom 500 view
handler403 = 'users.views.permission_denied'  # Replace with your app's custom 500 view
handler400 = 'users.views.bad_request'  # Replace with your app's custom 404 view

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

