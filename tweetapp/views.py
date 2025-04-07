from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import TweetForm, SignUpForm
from .models import Tweet
from django.contrib.auth.forms import AuthenticationForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'tweetapp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'tweetapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweetapp/home.html', {'tweets': tweets})

@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('home')
    else:
        form = TweetForm()
    return render(request, 'tweetapp/create_tweet.html', {'form': form})

@login_required
def update_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if tweet.user != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweetapp/update_tweet.html', {'form': form})

@login_required
def delete_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if tweet.user == request.user:
        tweet.delete()
    return redirect('home')
