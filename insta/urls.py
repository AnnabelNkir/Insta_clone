from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    # url(r'accounts/login/', auth_views.LoginView.as_view()),
    url('^$', views.index, name='home'),
    url(r'^home/$',views.index,name='index'),
    url(r'^new/image$', views.new_image, name='new-image'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^comment/(?P<image_id>\d+)', views.comment, name='comment'),
    url(r'^profiles/(\d+)',views.profiles,name='profiles'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
    #     views.activate, name='activate'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)