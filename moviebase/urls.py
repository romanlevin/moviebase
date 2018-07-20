from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
import rest_framework.routers
from api import views


router = rest_framework.routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
