from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.index, name='index'),
    url(r'^new/image$', views.new_image, name='new-image'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^comment/(?P<image_id>\d+)', views.comment, name='comment'),
    url(r'^profiles/(\d+)',views.profiles,name='profiles'),
   
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)