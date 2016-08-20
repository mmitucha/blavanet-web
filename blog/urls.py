from django.conf.urls import url

from . import views

urlpatterns = [
    # '',
    # url(r'^$', views.PostListView.as_view(), name="list"),
    url(r'^$', views.blog_index, name="blog-index"),
    url(r'^category/$', views.category_index, name="category-index"),
    url(r'^category/(?P<slug>[\w-]+)/$', views.category_posts, name="category-posts"),
    url(r'^post/(?P<slug>[\w-]+)/$', views.PostDetailView.as_view(), name="detail"),
]
