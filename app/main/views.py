from django.shortcuts import render, redirect, get_object_or_404
from .models import Tweet
from .models import Profile
from django.urls import reverse
from .forms import UserRegistrationForm , TweetForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .models import Tweet
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet, Reply,Story
from .forms import ReplyForm , StoryForm


def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def tweetlist(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    search_query = request.GET.get('search', '')
    
    if search_query:
        print("Search query:", search_query)  # Debug message
        search_results = Tweet.objects.filter(
            Q(content__icontains=search_query) |
            Q(user__username__icontains=search_query)
        ).distinct()

        if search_results.exists():
            tweets = search_results
        else:
            messages.error(request, f"No tweets found matching '{search_query}'.")

    # Fetch active stories (created within the last 24 hours)
    active_stories = Story.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('-created_at')
    
    context = {
        'tweets': tweets,
        'search_query': search_query,
        'all_stories': active_stories,
        # 'profile_url': reverse('profile', args=[request.user.id]) if request.user.is_authenticated else '#'
    }

    return render(request, 'tweet_list.html', context)



def reply_create(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.tweet = tweet
            reply.save()
            return redirect('tweetlist')  # Redirect to tweet list or tweet detail view
    else:
        form = ReplyForm()

    context = {
        'tweet': tweet,
        'form': form,
    }
    return render(request, 'tweet_list.html', context)

@login_required
def tweetcreate(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)  # Add request.FILES to handle file uploads
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user  # Assuming you have a user field in the Tweet model
            tweet.save()
            return redirect('tweet_detail', tweet_id=tweet.id)
    else:
        form = TweetForm()

    return render(request, 'form.html', {'form': form})
@login_required
def tweetedit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweetlist')
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'form.html', {'form': form})

def tweetdelete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweetlist')
    if request.method == 'POST':
        Reply.delete()
        return redirect('tweet_detail')
    return render(request, 'delete.html', {'tweet': tweet})

def login_page(request):
   
        # return render(request, 'login.html')
    return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  # Corrected this line
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweetlist')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect('login/')


def profile(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('tweetlist')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})



# views.py

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Tweet

@login_required
def user_tweets(request):
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_tweets.html', {'tweets': tweets})



@login_required
def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    replies = tweet.replies.all()
    # comments = Reply.objects.filter(tweet=tweet)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.tweet = tweet
            reply.user = request.user
            reply.save()
            return redirect('tweet_detail', tweet_id=tweet.id)
    else:
        form = ReplyForm()
    
    context = {
        'tweet': tweet,
        'replies': replies,
        # 'comments': comments,
        'form': form,
    }
    return render(request, 'tweet_detail.html', context)


def reply_delete(request, tweet_id, comment_id, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    # Check if the logged-in user is the author of the reply
    if reply.user == request.user:
        if request.method == 'POST':
            reply.delete()
            return redirect('tweet_detail', tweet_id=tweet_id)
        # Handle GET request to confirm deletion (optional)
        return render(request, 'delete.html', {'reply': reply})
    
    # Handle case where user is not authorized to delete the reply
    return redirect('tweet_detail', tweet_id=tweet_id)


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tweet

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)
        redirect('tweetlist')
    return redirect('tweet_detail', tweet_id=tweet.id)


def setting(request):
    return render(request,'setting.html')


@login_required
def Create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid:
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('tweetlist')

    else:
        form = StoryForm()
    return render(request, 'create_story.html', {'form':form})


# def stories(request):
#     all_stories = Story.objects.filter(created_at__gte=timezone.now())
#     return render(request,'tweetlist',{'stories':all_stories})