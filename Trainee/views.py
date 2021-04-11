from django.shortcuts import render,redirect
# Create your views here.
def traineeDash(request):
    print("Hello")
    return render(request,'traineeDashboard.html')

