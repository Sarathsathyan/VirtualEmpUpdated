from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Course,CreateCourse
from Admin.models import CategoryCourse,CareerCategory,SubCategory,RoleDetail
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
            return render(request, 'csmDashboard.html', context)
    else:
        messages.error(request, "Wrong URL")
        return redirect('logout')


    return render(request,'csmDashboard.html')

def chooseType(request):
    sub_cats = None
    data = None
    s_data = None
    s_courses = None
    c_data = None
    if request.method == 'POST':
        if 'category' in request.POST:
            category_id = request.POST['category']
            data = CareerCategory.objects.get(category=category_id)
            sub_cats = SubCategory.objects.filter(cat_id_id=data.pk)
        if 'first-sub' in request.POST:
            sub = request.POST['first-sub']
            s_data = SubCategory.objects.get(sub_category=sub)
            s_courses = CategoryCourse.objects.filter(sub_id_id=s_data.pk)
        if 'course' in request.POST:
            c_course = request.POST['course']
            c_data = CategoryCourse.objects.get(cfp=c_course)
        if 'course-submit' in request.POST:
            m_cat = request.POST['confirm_first_category']
            m_sub = request.POST['confirm_first_role']
            m_cfp = request.POST['course']
            print(m_cfp)
            data1 = CareerCategory.objects.get(category=m_cat)
            data2 = SubCategory.objects.get(sub_category=m_sub)
            data3 = CategoryCourse.objects.get(cfp=m_cfp)
            datas = CreateCourse(create_user_id=request.user.pk,create_category=data1.category,create_sub=data2.sub_category,
                                 create_course=data3.cfp)
            datas.save()
            messages.success(request, "Course Successfully Created Check Database")
            return redirect('csmAddCourse',datas.pk)
    cag_data = CareerCategory.objects.all()

    context = {
        'cag_data': cag_data,
        'sub_cats':sub_cats,
        'data':data,
        's_data':s_data,
        's_courses': s_courses,
        'c_data':c_data,

    }
    return render(request,'choseType.html',context)

def csmAddCourse(request,cat_id):
    if request.user.is_active:

        user = request.user
        inst = RoleDetail.objects.all()
        data = CreateCourse.objects.get(id = cat_id)
        if request.method == "POST":
            title = request.POST["title"]
            instructor = request.POST["instructor"]
            tagline = request.POST["tagline"]
            short_description = request.POST["description"]
            image = request.FILES.get('course_image')
            category = request.POST["category"]
            role = request.POST["role"]
            course = request.POST["course"]
            difficulty_level = request.POST["difficulty_level"]
            # lesson_title=request.POST["lesson_title"]
            # topic=request.POST["topic"]
            meta_keywords = request.POST["meta_keywords"]
            meta_description = request.POST["meta_description"]
            course_points = request.POST["course_points"]
            certificate = request.POST["certificate"]
            # quiz and certificate details are not added yet

            #  Prerequisites
            requirements = request.POST["req"]
            learnings = request.POST["learn"]

            create = Course(user_id=user.id, title=title, tagline=tagline, short_description=short_description,
                            instructor=instructor,
                            course_image=image, category_id=data.pk,
                            difficulty_level=difficulty_level, meta_keywords=meta_keywords,
                            meta_description=meta_description, course_points=course_points, certificate=certificate,
                            requirements=requirements, learnings=learnings)
            create.save()

            inst = RoleDetail.objects.all()

            return redirect("csmdashboard")
        context={
            'data':data,
            'inst':inst
        }
        return render(request,'csm_add_course.html',context)