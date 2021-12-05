from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from insta import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index,name= 'index'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)