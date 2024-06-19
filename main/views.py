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
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string



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
            Q(text__icontains=search_query) |
            Q(user__username__icontains=search_query)
        ).distinct()

        if search_results.exists():
            tweets = search_results
        else:
            messages.error(request, f"No tweets found matching '{search_query}'.")
    
    context = {
        'tweets': tweets,
        'search_query': search_query,
        # 'profile_url': reverse('profile', args=[request.user.id]) if request.user.is_authenticated else '#'
    }

    return render(request, 'tweet_list.html', context)


@login_required
def tweetcreate(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.photo = form.cleaned_data['photo']
            tweet.save()
            return redirect('tweetlist')
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
def user_tweets(request,username):
    user = get_object_or_404(User, username=username)

    # Retrieve tweets belonging to the logged-in user
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')

    # # Render the template with the tweets and user information
    return render(request, 'user_tweets.html', {'tweets': tweets, 'user': user})
    # tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    # return render(request, 'user_tweets.html', {'tweets': tweets})