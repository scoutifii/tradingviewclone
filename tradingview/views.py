from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import yfinance as yf
import pandas as pd
from datetime import datetime
from rest_framework.views import APIView
from .serializers import PostSerializers, CommentSerializers
from django.core.cache import cache
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import PostForm

url = 'dashboard.html'

# Define the ticker symbols
symbols = ['META', 'GOOGL', 'AAPL', 'MSFT', 'AMZN', 'ORCL', 'TSLA']

def index(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username) 
        # user_profile = Profile.objects.get(user=user_object)
        
    else:
        # user_profile = Profile.objects.all()
        # posts = Post.objects.all().order_by('-created_at') # Sorted by descending order
        # brand_setting = BrandSetting.objects.all()
        year = datetime.now().strftime("%Y")

    context = {
        # 'posts':posts,
        # 'user_profile':user_profile,
        # 'brand_setting':brand_setting,
        # 'year':year,
    }

    return render(request, 'index.html', context)

@login_required(login_url='login')
def dashboard(request):
    user_object = User.objects.filter(username=request.user.username)
    context = {
       'user_object': user_object
    }

    return render(request, 'dashboard.html', context)

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password == password_confirm:
            if User.objects.filter(email__iexact=email).exists():
                messages.info(request, 'Email Exists')
                return redirect('signup')
            elif User.objects.filter(username__iexact=username).exists():
                messages.info(request, 'Username Exists')
                return render(request, 'signup.html')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.save()
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                """#create a profile object for new user"""
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('dashboard')
                
        else:
            messages.info(request, 'Password Not Matching')
            return render(request, 'signup.html')
    else:
     return render(request, 'signup.html')

def track_login_attempts(request, username):
    attempts = cache.get(f'login_attempts_{username}', 0)
    cache.set(f'login_attempts_{username}', attempts + 1, 60 * 60)
    return attempts + 1  

def login(request):
    if request.user.is_authenticated:
        return redirect('settings')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            attempts = track_login_attempts(request, username)
            
            if attempts > 3:
                # Handle too many login attempts
                return render(request, "too_many_attempts.html") 
            
            user = auth.authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    cache.delete(f'login_attempts_{username}') 
                    
                    return redirect('dashboard')
                else:
                    messages.info(request, 'Account Deactivated')
            else:
                messages.info(request, 'Invalid username OR password')
                return redirect('login')
            
        return redirect('index')

@login_required(login_url='login')       
def logout(request):    
    auth.logout(request)
    return redirect('index')

# @login_required(login_url='login')
def market(request):
	url = "https://www.tradingview.com/symbols/BTCUSD/news/"
	response = requests.get(url)
	if response.status_code == 200:
		# data = response.json()
		print(response.text)
	else:
		print(f"Failed to retrieve data. status code: {response.status_code}")
	# context = {

	# }
	# return render(request, "", context)

@login_required(login_url='login')
def markets(request, symbol):
	context = {
	
	}
	return render(request, "", context)

def update_symbol_data(request):
    _get_posted_symbol_data()

    return render(request, "", {"Message": "Updated Successfully"})

def _get_posted_symbol_data():
    # Get data on the ticker
    for symbol in symbols:
        row = yf.Ticker(symbol)
        # Save on the database
        Symbol.objects.create(
            name = row.info['longName'],
            symbol = row.info["symbol"],
            slug = row.info["symbol"],
            exchange = row.info["exchange"],
            region = row.info["region"],
            currency = row.info["currency"],
            sector = row.info["sector"],
            industry = row.info["industry"]
        )

def update_ohlc_data(request, pk):
    _get_posted_ohlc_data(pk)

    return render(request, "update_ohlc_data.html", {"Message": "Updated Successfully"})

def _get_posted_ohlc_data(pk):
    symbol = Symbol.objects.get(id=pk)
    # Get data on the ticker 
    ticker = yf.Ticker(symbol.slug)
    # Get the historical prices for this ticker
    hist = ticker.history(period="1mo")
    for index, row in hist.iterrows():

        Ohlc.objects.create(
            symbol = symbol,
            timestamp = index,
            open = row["Open"],
            high = row["High"],
            low = row["Low"],
            close = row["Close"],
            volume = row["Volume"]
        )

def update_technical_data(request, pk):
    _get_posted_technical_data(pk)

    return render(request, "", {"message": "Updated Successfully"})

def _get_posted_technical_data(pk):
    # Get symbol ids 
    symbol = Symbol.objects.get(id=pk)
    # Get data on the ticker 
    ticker = yf.Ticker(symbol.slug)
    # Get the historical prices for this ticker
    hist = ticker.history(period="1mo")
    # Bollinger Bands
    hist['20 Day MA'] = hist['Close'].rolling(window=20).mean()
    hist['20 Day STD'] = hist['Close'].rolling(window=20).std()
    hist['Upper Band'] = hist['20 Day MA'] + (hist['20 Day STD'] * 2)
    hist['Lower Band'] = hist['20 Day MA'] - (hist['20 Day STD'] * 2)
    

    # Exponential Moving Averages
    hist['EMA12'] = hist['Close'].ewm(span=12, adjust=False).mean()
    hist['EMA26'] = hist['Close'].ewm(span=26, adjust=False).mean()

    # Moving Average Convergence Divergence
    hist['MACDline'] = hist['EMA12'] - hist['EMA26']
    hist['Signalline'] = hist['MACDline'].ewm(span=9, adjust=False).mean()
    hist['MACDHist'] = hist['MACDline'] - hist['Signalline']


    indicators = {
        '20 Day MA': '20 Day MA',
        'Upper Band': 'Upper Band',
        'Lower Band': 'Lower Band',
        'EMA12': 'EMA12',
        'EMA26': 'EMA26',
        'MACDline': 'MACDline',
        'Signalline': 'Signalline'
    }

    for index, row in hist.iterrows():
        for indicator, value in indicators.items():
            if indicator in row:
                Technical.objects.create(
                    symbol = symbol,
                    timestamp = index,
                    indicator = indicator,
                    value = row["Close"]
                )

def update_news_data(request, pk):
    _get_posted_news_data(pk)

    return render(request, "", {"message": "News updated successfully"})

def _get_posted_news_data(pk):
    # Get symbol ids 
    symbol = Symbol.objects.get(id=pk)
    # Get data on the ticker 
    ticker = yf.Ticker(symbol.slug)
    news = ticker.news

    try:
        article = news[0]
        title = article.get('content', {}).get('title')
        summary = article.get('content', {}).get('summary')
        link = article.get('content', {}).get('canonicalUrl').get('url')
        source = article.get('content', {}).get('canonicalUrl').get('url')
        published_at = article.get('content', {}).get('pubDate')

        News.objects.create(
            symbol = symbol,
            title = title,
            summary = summary,
            link = link,
            source = source,
            published_at = published_at
        )
    except IndexError:
        print("No news available")

def update_events_data(request, pk):
    _get_posted_events_data(pk)

    return render(request, "", {"message", "events updated successfully"})

def _get_posted_events_data(pk):
    # Get symbol ids 
    symbol = Symbol.objects.get(id=pk)
    # Get data on the ticker 
    ticker = yf.Ticker(symbol.slug)
    for key, value in ticker.calendar.items():
        if 'Earnings' in key:
            title = f"{symbol} Earnings"
            date = value
            if isinstance(date, list):
                date = value[0]
            else:
                date = value
            if isinstance(date, pd.Timestamp):
                date = date.strftime("%Y-%m-%d")
            event_type = "earnings" 
            impact_level = "high"

            Event.objects.create(
                symbol = symbol,
                title = title,
                date = date,
                event_type = event_type,
                impact_level = impact_level
            )

class PostView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return Response(status=204)
        except Post.DoesNotExist:
            return Response(status=404)


class CommentView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    def put(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response(status=204)
        except Comment.DoesNotExist:
            return Response(status=404)

@login_required(login_url="login")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user.pk
            post.user_prof = request.user.username
            post.save()
        # title = request.POST['title']
        # content = request.POST['content']
        # profile = request.POST.get['profile_id']
        # symbol = request.POST.get['symbol_id']
        # user = request.user.pk
        

        # post = Post.objects.create(
        #     title=title, 
        #     content=content, 
        #     profile_id=profile, 
        #     symbol_id=symbol, 
        #     user_id=user, 
        #     user_prof=user_prof
        # )
        # post.save()

        return redirect('dashboard')
    else:
        form = PostForm()   
    return render(request, 'create_post.html', {'form': form})



