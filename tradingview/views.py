from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from django.core.cache import cache
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.db.models import Q
from .helpers import timeago


url = 'dashboard.html'

# Define the ticker symbols
symbols = ['META', 'GOOGL', 'AAPL', 'MSFT', 'AMZN', 'ORCL', 'TSLA']

def index(request):
    year = datetime.now().strftime("%Y")

    context = {
        'year':year,
    }

    return render(request, 'index.html', context)

@login_required(login_url='login')
def dashboard(request):
    user_object = User.objects.filter(username=request.user.username)
    symbol = Symbol.objects.all()
    news = News.objects.select_related('symbol').all()
    context = {
       'user_object': user_object,
       'symbol': symbol,
       'news': news
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
def symbol(request, symbol):
    try:
        symbol = Symbol.objects.get(symbol=symbol)
        ohlc_data = Ohlc.objects.filter(symbol=symbol).values('timestamp', 'open', 'close', 'high', 'low', 'symbol__name', 'symbol__exchange', 'symbol__symbol', 'volume')
        news_data = News.objects.filter(symbol=symbol).values('created_at', 'title', 'source')
        technical_data = Technical.objects.filter(symbol=symbol).values('indicator', 'value')
        data = {
            'symbol_name': [obj['symbol__name'] for obj in ohlc_data],
            'symbol': [obj['symbol__symbol'] for obj in ohlc_data],
            'exchange': [obj['symbol__exchange'] for obj in ohlc_data],
            'labels': [obj['timestamp'].strftime('%H:%M') for obj in ohlc_data],
            'volume': [obj['volume'] for obj in ohlc_data],
            'high': [obj['high'] for obj in ohlc_data],
            'low': [obj['low'] for obj in ohlc_data],
            'datasets': [
                {
                    'label': 'Open',
                    'data': [obj['open'] for obj in ohlc_data],
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                },
                {
                    'label': 'Close',
                    'data': [obj['close'] for obj in ohlc_data],
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                },
            ],
            
            'created_at': [obj['created_at'].strftime('%H:%M') for obj in news_data],
            'title': [obj['title'] for obj in news_data],
            'source': [obj['source'] for obj in news_data],
            'indicator': [obj['indicator'] for obj in technical_data],
            'value': [obj['value'] for obj in technical_data],
        }
        return JsonResponse({'symbol_chart': data})
    except Symbol.DoesNotExist:
        return JsonResponse({'error': 'Symbol not found'})
    
    

class SymbolChartView(TemplateView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['symbol'] = self.kwargs['symbol']
        return context


@login_required(login_url='login')
def market(request):
    if request.method == 'POST':
        symbol = request.POST['q']
        
        return redirect(f'market/{symbol}')

def autosuggest(request):
    if 'term' in request.GET: 
        search_term = request.GET.get('term')       
        symbols = Symbol.objects.filter(
            Q(symbol__icontains=search_term) 
        )
        payload = [f"{obj.symbol}" for obj in symbols]
    
    return JsonResponse(payload, safe=False)

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

    return render(request, "", {"Message": "Updated Successfully"})

def _get_posted_ohlc_data(pk):
    symbol = Symbol.objects.get(id=pk)
    # Get data on the ticker 
    ticker = yf.Ticker(symbol.slug)
    # Get the historical prices for this ticker
    hist = ticker.history(period="1y")
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
    hist = ticker.history(period="1y")
    # Bollinger Bands
    hist['20 Day MA'] = hist['Close'].rolling(window=20).mean()
    hist['20 Day STD'] = hist['Close'].rolling(window=20).std()
    hist['Upper Band'] = hist['20 Day MA'] + (hist['20 Day STD'] * 2)
    hist['Lower Band'] = hist['20 Day MA'] - (hist['20 Day STD'] * 2)    

    # Exponential Moving Averages
    hist['EMA10'] = hist['Close'].ewm(span=10, adjust=False).mean()
    hist['EMA20'] = hist['Close'].ewm(span=20, adjust=False).mean()
    hist['EMA30'] = hist['Close'].ewm(span=30, adjust=False).mean()
    hist['EMA50'] = hist['Close'].ewm(span=50, adjust=False).mean()

    # Moving Average Convergence Divergence
    hist['MACDline'] = hist['EMA10'] - hist['EMA20']
    hist['Signalline'] = hist['MACDline'].ewm(span=9, adjust=False).mean()
    hist['MACDHist'] = hist['MACDline'] - hist['Signalline']


    indicators = {
        '20 Day MA': '20 Day MA',
        'Upper Band': 'Upper Band',
        'Lower Band': 'Lower Band',
        'EMA12': 'EMA10',
        'EMA26': 'EMA20',
        'EMA12': 'EMA30',
        'EMA26': 'EMA50',
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
        created_at = article.get('content', {}).get('pubDate')

        News.objects.create(
            symbol = symbol,
            title = title,
            summary = summary,
            link = link,
            source = source,
            created_at = created_at
        )
    except IndexError:
        print("No news available")

def update_events_data(request, pk):
    _get_posted_events_data(pk)

    return render(request, "", {"message", "events updated successfully"})

def _get_posted_events_data(pk):
    try:
        # Get symbol ids 
        symbol = Symbol.objects.get(id=pk)
        # Get data on the ticker 
        ticker = yf.Ticker(symbol.slug)
        calendar = ticker.calendar
        info = ticker.info

        if calendar is not None:
            for key, value in calendar.items():
                if 'Earnings' in key:
                    title = f"{symbol} Earnings"
                    date = value
                    if isinstance(date, list):
                        date = date[0]
                    else:
                        date = value
                    if isinstance(date, pd.Timestamp):
                        date = date.date()

                    event_type = "earnings"
                    market_cap = info.get('manketCap')
                    impact_level = "high" if market_cap and not np.isnan(market_cap) and market_cap > 100000000000 else "low"

                    if date is not None:
                        Event.objects.create(
                            symbol = symbol,
                            title = title,
                            date = date,
                            event_type = event_type,
                            impact_level = impact_level
                        )
    except Symbol.DoesNotExist:
        print(f"Symbol with id {pk} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


@login_required(login_url="login")
def create_post(request, pk):
    try:
        symbol = Symbol.objects.get(id=pk)
        user_object = User.objects.get(id=request.user.id) 
        user_profile = Profile.objects.get(user=user_object)
    except(Symbol.DoesNotExist, User.DoesNotExist, Profile.DoesNotExist):
        return redirect('error_page')
        if request.method == 'POST': 
            content = request.POST['content']

            post = Post.objects.create(
                content=content, 
                profile=user_profile, 
                symbol=symbol, 
                user=request.user.pk, 
                user_prof=request.user.username
            )
            post.save()

            return JsonResponse({'message': 'Post created successfully'})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_symbol_id(request, symbol):
    try:
        symbol_obj = Symbol.objects.get(symbol=symbol)
        return JsonResponse({'id': symbol_obj.id})
    except Symbol.DoesNotExist:
        return JsonResponse({'error': 'Symbol not found'}, status=404)

def get_symbol_events(request):
    events = Event.objects.values('date', 'event_type', 'impact_level', 'title').distinct()
    return JsonResponse({'events': list(events)})


class EventsView(TemplateView):
    template_name = 'events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context