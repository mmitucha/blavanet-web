from django.views.generic import TemplateView
from django.shortcuts import render
# from django.http import Http404, Http500


class HomePageView(TemplateView):
    template_name = "homepage.html"


def custom_404(request):
    return render(request, '404.html', status=404)
    # raise Http404('404.html')


def custom_500(request):
    return render(request, '500.html', status=500)
    # raise Http500('500.html')
