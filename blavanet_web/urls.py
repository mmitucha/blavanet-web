from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.HomePageView.as_view(), name="home"),
    url(r'^blog/', include("blog.urls", namespace="blog")),
)

urlpatterns += patterns(
    'django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
    url(r'^contact/$', 'flatpage', {'url': '/contact/'}, name='contact'),
)

handler404 = "blavanetproject.views.custom_404"
handler500 = "blavanetproject.views.custom_500"
