from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_tweet, name='create_tweet'),
    path('update/<int:pk>/', views.update_tweet, name='update_tweet'),
    path('delete/<int:pk>/', views.delete_tweet, name='delete_tweet'),
]
