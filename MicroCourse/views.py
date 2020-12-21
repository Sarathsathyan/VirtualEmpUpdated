from django.shortcuts import render

# Create your views here.

def microDash(request):
    return render(request,'microDashboard.html')
