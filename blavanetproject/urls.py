from django.conf.urls import patterns, include, url, handler404, handler500
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blavanetproject.views.home', name='home'),
    # url(r'^blavanetproject/', include('blavanetproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', views.HomePageView.as_view(), name="home"),
    url(r'^blog/', include("blog.urls", namespace="blog")),

    # (r'^about/', include('django.contrib.flatpages.urls')),
    # (r'^(?P<url>.*/)$', 'django.contrib.flatpages.views.flatpage'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
    url(r'^contact/$', 'flatpage', {'url': '/contact/'}, name='contact'),
)

handler404 = "blavanetproject.views.custom_404"
handler500 = "blavanetproject.views.custom_500"
