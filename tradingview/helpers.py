from .models import SyncLog
from datetime import datetime
# from django.utils.deprecation import MiddlewareMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

class SyncLog:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		start_time = timezone.now()
		response = self.get_response(request)
		self.process_response(request, response, start_time)
		return response


	def process_response(self, request, response, start_time):
		try:
			activity = SyncLog()
			activity.api_name = request.META['PATH_INFO']
			activity.last_run = start_time
			activity.status = 'success' if response.status_code < 400 else 'failure'
			activity.error_message = '' if response.status_code < 400 else str(response)
			activity.duration_seconds = (timezone.now() - start_time).total_seconds()
			activity.save()
		except Exception as e:
			print(f"Error logging request: {e}")

		return response