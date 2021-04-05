from django.shortcuts import render

# Create your views here.
def major_project_dashboard(request):
    return render(request,'major_project_dashboard.html')

def project_creation(request):
    return render(request,'project_creation.html')
