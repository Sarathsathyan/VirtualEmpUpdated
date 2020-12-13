from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Course,CreateCourse
# Create your views here.

def csmDashboard(request):
    if request.user.is_active:
        if request.method == 'POST':
            if 'courseDelete' in request.POST:
                print("Delete Course")
                c_id = request.POST['del_id']
                try:
                    course_del = Course.objects.get(id=c_id).delete()
                    messages.success(request, "Deleted successfully")
                except:
                    messages.error(request, "Some error occured")

        if request.user.is_authenticated:
            allCourses = Course.objects.filter(user=request.user)
            for i in allCourses:
                print(i.id)
            context = {
                'courses': allCourses,
            }
            return render(request, 'CSM/csmDashboard.html', context)
    else:
        messages.error(request, "Wrong URL")
        return redirect('logout')


    return render(request,'CSM/csmDashboard.html')
