# provet/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # / maps to upload()
    path('', include('autoconsul.urls')),
    path('admin/', admin.site.urls),
    path('celery-progress/', include('celery_progress.urls')),
]
