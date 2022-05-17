from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'goscp_site/home.html')