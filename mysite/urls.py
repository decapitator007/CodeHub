from django.contrib import admin
from django.urls import path,include
urlpatterns=[
    path('admin/',admin.site.urls),
    path('',include('CodeHub.urls')),
]
handler404='CodeHub.views.error_404'
