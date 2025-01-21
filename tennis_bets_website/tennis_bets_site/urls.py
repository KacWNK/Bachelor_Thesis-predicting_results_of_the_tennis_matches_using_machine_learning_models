from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),           # Admin page
    path('stats/', include('stats.urls')),     # Include stats app's URLs under the /stats/ path
]