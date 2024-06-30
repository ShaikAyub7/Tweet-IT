from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweetlist, name='tweetlist'),
    path('create/', views.tweetcreate, name='tweetcreate'),
    path('tweet/<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),
    path('<int:tweet_id>/edit/', views.tweetedit, name='tweetedit'),
    path('<int:tweet_id>/delete/', views.tweetdelete, name='tweetdelete'),
    # path('<int:tweet_id>/delete/', views.tweetdelete, name='tweetdelete'),
    path('<int:tweet_id>/<int:comment_id>/<int:reply_id>/delete/', views.reply_delete, name='reply_delete'),
    path('profile/', views.profile, name='profile'),
    path('tweet/<int:tweet_id>/reply/', views.reply_create, name='reply_create'),
    path('profile/<int:user_id>/', views.profile, name='profile_with_id'),
    path('user/', views.user_tweets, name='user_tweets'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login.html'),
    path('logout/', views.logout_page, name='logout'),
    path('tweet/<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),
    path('setting/',views.setting,name='setting.html')

]