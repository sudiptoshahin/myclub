
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    # default authentications urls
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
]

# Configure admin titles
admin.site.site_header = "My Club admin page"
admin.site.site_title = "Browser Title"
# admin.site.index_title = "Welcome to admin"
admin.site.index_title = ""