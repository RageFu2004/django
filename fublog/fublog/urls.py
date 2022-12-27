"""fublog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from user import views as user_views
from dtoken import views as dtoken_views
from message import views as message_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('test_cors', views.test_cors),
    # django built-in View.as_view() can return a function
    path('v1/users', user_views.UserViews.as_view()),
    path('v1/users/', include('user.urls')),
    path('v1/tokens', dtoken_views.tokens),
    path('v1/topics/', include('topics.urls')),
    path('v1/messages/<str:topic_id>', message_views.message_view)
]
# first arg is the static file's request URL, second is the storage directory in django
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
