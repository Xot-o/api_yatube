from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import PostViewSet, CommentViewSet, api_group, api_group_detail
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('posts/', PostViewSet, basename='posts')
router.register('posts/<int:post_id>/comments/', CommentViewSet, basename='comments')

urlpatterns = [

    path('api-token-auth/', views.obtain_auth_token),
    path('groups/', api_group),
    path('groups/<int:pk>', api_group_detail),

]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
