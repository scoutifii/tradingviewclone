from .models import SyncLog
from datetime import datetime
from django.utils import timezone
import math
from django.http import HttpResponse


class SyncLog:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def process_request(self, request):
		try:
			activity = SyncLog()
			activity.api_name = request.META['PATH_INFO']
			activity.last_run = timezone.now()
			activity.status = 'success' if HttpResponse.status_code < 400 else 'failure'
			activity.error_message = '' if HttpResponse.status_code < 400 else 'error'
			activity.duration_seconds = (timezone.now() - start_time).total_seconds()
			activity.save()
		except Exception as e:
			raise e

		return None


def timeago(self):
	now = timezone.now()
	diff= now - self.created_at

	if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
		seconds= diff.seconds

		if seconds == 1:
			return str(seconds) +  "s"
		else:
			return str(seconds) + "seconds"
	if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
		minutes= math.floor(diff.seconds/60)

		if minutes == 1:
			return str(minutes) + "m"
		else:
			return str(minutes) + "minutes"

	if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
		hours= math.floor(diff.seconds/3600)

		if hours == 1:
			return str(hours) + "h"
		else:
			return str(hours) + "hours"

	if diff.days >= 1 and diff.days <= 6:
		days= diff.days

		if days == 1:
			return str(days) + "d"
		else:
			return str(days) + "days"

	if diff.days >= 7 and diff.days < 31:
		weeks= math.floor(diff.days/7)

		if weeks == 1:
			return str(weeks) + "week"
		else:
			return str(weeks) + "weeks"

	if diff.days >= 31 and diff.days < 365:
		months= math.floor(diff.days/31)

		if months == 1:
			return str(months) + "month"
		else:
			return str(months) + "months"

	if diff.days >= 365:
		years= math.floor(diff.days/365)

		if years == 1:
			return str(years) + "y"
		else:
			return str(years) + "years"
