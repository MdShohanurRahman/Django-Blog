from django.contrib import admin
from django.urls import path, include
from blog import views
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('blog/<id>/<slug>/', views.post_details, name='post_details'),
    path('post_create/', views.post_create, name='post_create'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('likes/', views.like_post, name='like_post'),

    # password reset urls
    # path('password_reset',auth_views.password_reset,name='password_reset'),
    # path('password_reset/done',auth_views.password_change_done,name='password_reset_done'),
    # path('password_reset/confirm/<uidb64>/<token>',auth_views.password_reset_confirm,name='password_reset_confirm'),
    # path('password_reset/complite/',auth_views.password_reset_complete,name='password_reset_complite'),

    path('', include('django.contrib.auth.urls')),

]
