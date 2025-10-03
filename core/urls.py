
from django.contrib import admin
from django.urls import path, include

from api.views import login_view

import api

urlpatterns = [
    path('', login_view, name='login_page'),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
