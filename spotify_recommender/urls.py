from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from recommender.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('recommender/', include('recommender.urls')),
    path('', dashboard, name='home'),
    path('recommender/', include('recommender.urls')),
]