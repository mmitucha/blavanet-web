from django.views.generic import TemplateView
from django.shortcuts import render

class HomePageView(TemplateView):
    template_name = "homepage.html"


def custom_404(request):
   return render(request, '404.html')

def custom_500(request):
    return render(request,'500.html')
