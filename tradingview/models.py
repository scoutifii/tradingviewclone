from django.db import models
from django.contrib.auth.models import User
import uuid


class Symbol(models.Model):
	SYMBOL_TYPES = (("stock", 'Stock'), ("crypto", 'Cryptocurrency'), ("forex", 'Forex'), ("commodity", 'Commodity'), ("index", 'Index'))
	name = models.CharField(max_length=100)
	symbol = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, unique=True)
	exchange = models.CharField(max_length=100)
	region = models.CharField(max_length=100)
	currency = models.CharField(max_length=100)
	sector = models.CharField(max_length=100)
	industry = models.CharField(max_length=100)
	isin = models.CharField(max_length=100)
	active = models.BooleanField(default=True)
	type = models.CharField(choices=SYMBOL_TYPES, max_length=100, default='stock')
	created_at= models.DateTimeField(auto_now_add=True)


	class Meta:
		db_table = "symbol"

	def __str__(self):
		return f"{self.name}"

class Ohlc(models.Model):
	symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="ohlc")
	timestamp = models.DateTimeField(auto_now_add=True)
	open = models.FloatField(max_length=10, null=True, blank=True, default=0.0)
	high = models.FloatField(max_length=10, null=True, blank=True, default=0.0) 
	low = models.FloatField(max_length=10, null=True, blank=True, default=0.0) 
	close = models.FloatField(max_length=10, null=True, blank=True, default=0.0) 
	volume = models.FloatField(max_length=10, null=True, blank=True, default=0.0)

	class Meta:
		db_table = "ohlc"

	def __str__(self):
		return f"{self.timestamp}"


class Technical(models.Model):
	INDICATORS = (("rsi", 'RSI'), ("macd", 'MACD'))
	symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="technical")
	indicator = models.CharField(choices=INDICATORS, max_length=15)
	value = models.FloatField(max_length=10, null=True, blank=True, default=0.0)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "technical"

class News(models.Model):
	symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="news")
	title = models.CharField(max_length=100)
	summary = models.TextField()
	link = models.URLField(max_length=200, blank=True, null=True)
	source = models.CharField(max_length=200, blank=True, null=True)
	published_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "news"

	def __str__(self):
		return f"{self.title}"

class Event(models.Model):
	EVENT_TYPES = (("earnings", 'Earnings'), ("split", 'Split'), ("fork", 'Fork'), ("other", 'Other'))
	IMPACT_LEVELS = (("low", 'Low'), ("medium", 'Medium'), ("high", 'High'))
	symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="events")
	title = models.CharField(max_length=100, blank=True, null=True)
	date = models.DateField()
	event_type = models.CharField(choices=EVENT_TYPES, max_length=100, blank=False)
	impact_level = models.CharField(choices=IMPACT_LEVELS, max_length=100, blank=False)

	class Meta:
		db_table = "event"

	def __str__(self):
		return f"{self.symbol}"

class SyncLog(models.Model):
	STATUS = (("success", 'Success'), ("failure", 'Failure'))

	api_name = models.CharField(max_length=100)
	last_run = models.DateTimeField(auto_now_add=True)
	status = models.CharField(choices=STATUS, max_length=15, blank=False)
	error_message = models.TextField()
	duration_seconds = models.FloatField(max_length=10, null=True, blank=True, default=0.0)

	class Meta:
		db_table = "sync_log"

class WatchList(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
	symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="watchlists")


	class Meta:
		db_table = "watch_list"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile') 
    id_user = models.IntegerField() #Primary key of profile
    bio = models.TextField(blank=True)
    phone_no = models.CharField(max_length=13, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "profile"
    
    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    uuid = models.CharField(max_length=255, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, default=None, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_prof = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "post"

    def __str__(self):
        return f"{self.user}, {self.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name="comments")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, default=None, related_name='comments')
    user_prof = models.CharField(max_length=50, blank=True, default=None)
    comment_body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return '%s - %s' % (self.post.post_name, self.comment_body)

