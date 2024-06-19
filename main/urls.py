from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.tweetlist, name='tweetlist'),
    path('create/', views.tweetcreate, name='tweetcreate'),
    path('<int:tweet_id>/edit/', views.tweetedit, name='tweetedit'),
    path('<int:tweet_id>/delete/', views.tweetdelete, name='tweetdelete'),
    path('profile/',views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile_with_id'),
    path('tweet/<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),
    # path('tweet/<int:tweet_id>/', tweet_detail, name='tweet_detail'),
    path('user/', views.user_tweets, name='user_tweets'),
    path('register/',views.register,name='register'),
    path('login/',views.login_page,name='login.html'),
    path('logout/',views.logout_page,name='logout'),

    
]
