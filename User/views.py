from django.shortcuts import render
from django.contrib import messages

from Admin.models import (UserDetails,CareerCategory,SubCategory,CategoryCourse)
from .models import CareerChoice
# Create your views here.

# CSM

def userCfp(request):
    user = request.user
    details = UserDetails.objects.get(user_id_id=user.pk)
    sub_cats = None
    s_courses = None
    data = None
    s_data = None
    c_data = None
    if request.method == 'POST':
        if 'first-category' in request.POST:
            category_id = request.POST['first-category']
            data = CareerCategory.objects.get(id=category_id)
            sub_cats = SubCategory.objects.filter(cat_id_id=data.pk)
        if 'first-sub' in request.POST:
            sub = request.POST['first-sub']
            s_data = SubCategory.objects.get(sub_category=sub)
            s_courses = CategoryCourse.objects.filter(sub_id_id=s_data.pk)
        if 'course' in request.POST:
            c_course = request.POST['course']
            c_data = CategoryCourse.objects.get(cfp=c_course)
        if 'confirm_submit' in request.POST:
            m_cat = request.POST['confirm_first_category']
            m_sub = request.POST['confirm_first_role']
            m_cfp = request.POST['confirm_first_cfp']
            data1 = CareerCategory.objects.get(category=m_cat)
            data2 = SubCategory.objects.get(sub_category=m_sub)
            data3 = CategoryCourse.objects.get(cfp=m_cfp)
            data = CareerChoice(cat_id_id=data1.pk, sub_id_id=data2.pk, cfp_id_id=data3.pk, user_id_id=user.pk)
            data.save()
            messages.success(request, "CFP choosed")
    career_list = CareerCategory.objects.all()

    context = {
        'career_list': career_list,
        'sub_cats': sub_cats,
        's_courses': s_courses,
        'data': data,
        's_data': s_data,
        'c_data': c_data
    }
    return render(request, 'userCFP.html', context)

def userDashboard(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        user_details = UserDetails.objects.get(user_id_id=user.pk)


    return render(request,'userDashboard.html')


def csmDashboard(request):
    return render(request,'CSM/csmDashboard.html')