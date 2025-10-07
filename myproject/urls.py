from django.contrib import admin
from django.urls import path, include
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('helloword/', views.helloword),
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('shakhzot/', views.defshakhzot, name='shakhzot'),
    path('shakhzot/add/', views.add, name='add'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name='login'), 
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/profile/<str:username>/edit/', views.profile_edit, name='profile_edit'),
    path('accounts/profile/<str:username>/', views.profile_view, name='profile'),
    path('create', views.create_post, name='create_post'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)