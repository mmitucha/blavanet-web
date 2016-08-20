from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.HomePageView.as_view(), name="home"),
    url(r'^blog/', include("blog.urls", namespace="blog")),
]

urlpatterns += [
    # url(r'^about/$', include('django.contrib.flatpages.urls'), name='about'),
    # url(r'^contact/$', include('django.contrib.flatpages.urls'), name='contact'),
    url(r'^about/', include('django.contrib.flatpages.urls')),
    url(r'^contact/', include('django.contrib.flatpages.urls')),
]

urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "blavanet_web.views.custom_404"
handler500 = "blavanet_web.views.custom_500"
