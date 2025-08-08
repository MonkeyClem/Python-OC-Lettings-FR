from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lettings/', include('lettings.urls', namespace='lettings')),
    path('lettings/<int:letting_id>/', views.letting, name='letting'),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('profiles/<str:username>/', views.profile, name='profile'),
    path('admin/', admin.site.urls),
]
