from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PublishedPostsMixin(object):
    def get_queryset(self):
        return(self.model.objects.live())


class PostListView(PublishedPostsMixin, ListView):
    model = Post


class PostDetailView(PublishedPostsMixin, DetailView):
    model = Post


def blog_index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return(render(request, 'blog/blog_index.html', {
        'categories': Category.objects.all(),
        'posts': posts}))


def category_index(request):
    return(render(request, 'blog/category_index.html', {
        'categories': Category.objects.all()}))


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    post_list = Post.objects.filter(category=category)
    paginator = Paginator(post_list, 5)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return(render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts}))


# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def listing(request):
#     contact_list = Contacts.objects.all()
#     paginator = Paginator(contact_list, 25) # Show 25 contacts per page

#     page = request.GET.get('page')
#     try:
#         contacts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         contacts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         contacts = paginator.page(paginator.num_pages)

#     return render_to_response('list.html', {"contacts": contacts})
