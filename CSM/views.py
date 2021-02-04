import random
import re
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Course,CreateCourse,Week_Unit,Week,Quizz
from Admin.models import CategoryCourse,CareerCategory,SubCategory,RoleDetail
import datetime
# Create your views here.
from moviepy.editor import VideoFileClip

def csmDashboard(request):
    if request.user.is_active:
        if request.method == 'POST':
            if 'courseDelete' in request.POST:
                print("Delete Course")
                c_id = request.POST['del_id']
                
                c_id=int(c_id[4:])
                print("c_id is ",c_id)
                
                try:

                    course_object=Course.objects.get(id=c_id)
                    cat_id=course_object.category.id
                    #print(cat_id)
                    createcourse_del=CreateCourse.objects.get(id=cat_id).delete()
                    #course_del = Course.objects.get(id=c_id).delete()
                    course_del = course_object.delete()
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
            print(category_id)
            data = CareerCategory.objects.get(category=category_id)
            print(data)
            print(data.pk)
            #sub_cats = SubCategory.objects.filter(cat_id_id=data.pk)
            #print(sub_cats = SubCategory.objects.filter(cat_id_id=data.pk))
            sub_cats = SubCategory.objects.filter(cat_id=data.pk)
            print(sub_cats)
        if 'first-sub' in request.POST:
            sub = request.POST['first-sub']
            #print(sub)
            s_data = SubCategory.objects.get(sub_category=sub)
            #print(s_data)
            s_courses = CategoryCourse.objects.filter(sub_id_id=s_data.pk)
            #print(s_courses)
        if 'course' in request.POST:
            c_course = request.POST['course']
            #print(c_course)
            c_data = CategoryCourse.objects.get(cfp=c_course)
            #print(c_data)
        if 'course-submit' in request.POST:
            m_cat = request.POST['confirm_first_category']
            #print("m_cat: ", m_cat)
            m_sub = request.POST['confirm_first_role']
            #print("m_sub: ", m_sub)
            m_cfp = request.POST['course']
            #print(m_cfp)
            data1 = CareerCategory.objects.get(category=m_cat)
            #print("data1: ",data1)
            data2 = SubCategory.objects.get(sub_category=m_sub)
            #print("data2: ", data2)
            data3 = CategoryCourse.objects.get(cfp=m_cfp)
            #print("data3: ",data3)
            datas = CreateCourse(create_user_id=request.user.pk,create_category=data1.category,create_sub=data2.sub_category,
                                 create_course=data3.cfp)
            datas.save()
            #print("datas: ",datas)
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
            xp_points=request.POST["xp_points"]

            xp_points = request.POST["xp_points"]

            certificate = request.FILES.get('certificate')
            # quiz and certificate details are not added yet

            #  Prerequisites
            requirements = request.POST["req"]
            learnings = request.POST["learn"]

            create = Course(user_id=user.pk, title=title, tagline=tagline, short_description=short_description,
                            instructor=instructor,course_image=image, category_id=data.pk,
                            difficulty_level=difficulty_level, meta_keywords=meta_keywords,
                            meta_description=meta_description, course_points=course_points,
                            xp_points_perq=xp_points_perq, certificate=certificate,xp_points=xp_points,
                            requirements=requirements, learnings=learnings)
            create.save()

            inst = RoleDetail.objects.all()

            return redirect("csmdashboard")
        context={
            'data':data,
            'inst':inst
        }
        return render(request,'csm_add_course.html',context)

def csmEdit(request, course_id):
    if request.user.is_active:
        course_object=Course.objects.filter(user=request.user)
        Course_name = course_object.get(id=course_id)
        inst=RoleDetail.objects.all()
        if request.method=="POST":
            Course_name.title = request.POST["title"]
            Course_name.instructor = request.POST["instructor_name"]
            Course_name.tagline = request.POST["tagline"]
            Course_name.short_description = request.POST["description"]
            Course_name.meta_keywords = request.POST["meta_keywords"]
            Course_name.meta_description = request.POST["meta_description"]
            image_file= request.FILES.get('course_image')
            print("image_file",image_file)
            Course_name.difficulty_level = request.POST["difficulty_level"]
            Course_name.course_points = request.POST["course_points"]

            Course_name.xp_points_perq = request.POST["xp_points_perq"]
            Course_name.xp_points= request.POST["xp_points"]
            Course_name.xp_points = request.POST["xp_points"]
            certificate = request.FILES.get('certificate')

            Course_name.modified=datetime.datetime.now()
            if  image_file:
                Course_name.course_image =image_file
            else:
                if not Course_name.course_image:
                    message="Please select an image"
                    return redirect("csmEdit",course_id)

                    #return render(request,'csm_edit_course.html',{"message":message})
            if  certificate:
                Course_name.certificate =certificate
            else:
                if not Course_name.certificate:
                    message="Please select an image"
                    return redirect("csmEdit",course_id)

            Course_name.difficulty_level = request.POST["difficulty_level"]
            
            Course_name.requirements = request.POST["req"]
            Course_name.learnings = request.POST["learn"]
            
            Course_name.save()
            inst=RoleDetail.objects.all()
            messages.success(request, "Course Edited Successfully!")
            return redirect("csmdashboard")
        f_req, s_req, l_req =re.split("_",Course_name.requirements)
        print("first ",f_req)
        print("second ",s_req)
        print("third ",l_req)
        f_learn, s_learn, l_learn =re.split("_",Course_name.learnings)
        first=Course_name.requirements
        print(first)
        context={
            'data': Course_name,
            'inst': inst,
            'f_req':f_req, 
            's_req':s_req, 
            'l_req':l_req,
            'f_learn':f_learn, 
            's_learn':s_learn, 
            'l_learn':l_learn
        }
        print(Course_name)
        print(Course_name.category.create_category)
        return render(request,'csm_edit_course.html', context)
    else:
        return render("login")

# function to find duration of video
def video_duration(seconds):
    hours=seconds//3600
    seconds%=3600
    minutes=seconds//60
    seconds%=60
    return f"{hours}:{minutes}:{seconds}"    


def csmAddCurriculam(request,curr_id):
    if request.user.is_active:

        Course_name = Course.objects.get(id=curr_id)
        course_title = Course_name.title
        if request.method == 'POST':
            if 'create' in request.POST:
                week_name = request.POST['week']
                if Week.objects.filter(week_id_id=curr_id, week_name=week_name).exists():
                    messages.error(request, "Week name already exists")
                    return redirect('csmAddCurriculam', id)
                week_private = random.randint(112, 1000) * 100
                data = Week(week_name=week_name, week_private=week_private, week_id_id=curr_id)
                data.save()
                messages.success(request, "Week Added")
                print("success")

            if 'addWeekUnit' in request.POST:
                unit_caption = request.POST['unit_caption']
                unit_captionOne = request.POST['unit_captionOne']
                unit_captionTwo = request.POST['unit_captionTwo']
                unit_captionThree = request.POST['unit_captionThree']
                unit_video1 = request.FILES.get('unit_video1')
                unit_video2 = request.FILES.get('unit_video2')
                unit_video3 = request.FILES.get('unit_video3')
                week = request.POST['wek_id']
                if unit_video1:
                    clip1=VideoFileClip(unit_video1.temporary_file_path())
                    video1_duration=video_duration(int(clip1.duration))
                else:
                    video1_duration=None
                if unit_video2:
                    clip2=VideoFileClip(unit_video2.temporary_file_path())
                    video2_duration=video_duration(int(clip2.duration))
                else:
                    video2_duration=None
                if unit_video3:
                    clip3=VideoFileClip(unit_video3.temporary_file_path())
                    video3_duration=video_duration(int(clip3.duration))
                else:
                    video3_duration=None
                try:
                    week_private = Week.objects.get(week_private=week)
                    if week_private:
                        print("enter")
                        if Week_Unit.objects.filter(unit_id_id=week_private.pk,unit_caption=unit_caption).exists():
                            messages.error(request, "Unit name already exists")
                            return redirect('csmAddCurriculam', id)
                        print("hellooo")
                        unit = Week_Unit(unit_id_id=week_private.pk,unit_video1=unit_video1, unit_video2=unit_video2, unit_video3=unit_video3,
                                       uCapOne=unit_captionOne,u_capThree=unit_captionThree,uCap2=unit_captionTwo,
                                       video1_duration=video1_duration, video2_duration=video2_duration,video3_duration=video3_duration)
                        unit.save()
                        
                        messages.success(request, "Unit added to week")
                    else:
                        messages.error(request, "Wrong Lesson Id")
                except:
                    print("error")
                    messages.error(request, "Some error occured")
            if 'del' in request.POST:
                print("delete")
                del_id = request.POST['l_id']
                try:
                    lesson_del = Lesson.objects.get(id=del_id).delete()
                    topic_del = Lesson_Topic.objects.filter(topic_id_id=del_id)
                    messages.success(request, "Deleted successfully")
                except:
                    messages.error(request, "Some error occured")

        #weeks = Week.objects.order_by("week_name")
        weeks=Week.objects.all()
        context = {
            'weeks': weeks,
            'course_title': course_title,
            'c_id': curr_id,
        }
        print(course_title)
        return render(request, 'csm_add_curriculam.html', context)


    else:
        messages.error(request,"Wrong url")
        return redirect('/login')

def csmAddQuizz(request,w_id):
    user = request.user
    datas = Quizz.objects.filter(week_id_id=w_id)
    week = Week.objects.get(id = w_id)
    course = Course.objects.get(id = week.week_id_id)

    if request.method == 'POST':
        if 'save' in request.POST:
            question = request.POST['question']
            que1 = request.POST['answer1']
            que2 = request.POST['answer2']
            que3 = request.POST['answer3']
            que4 = request.POST['answer4']
            ans = request.POST['ans']
            my_json = {"A": que1, "B": que2, "C": que3, "D": que4}

            data = Quizz(week_id_id=w_id, question=question, answer=ans, option1=que1, option2=que2, option3=que3,
                         option4=que4, ques_no=datas.count() + 1,course_id_id=course.pk,option=my_json)

            data.save()
            messages.success(request, "Question added")
            return redirect('csmAddQuizz', w_id)




    context = {
        'w_id':w_id,
        'data': datas,
        'quiz_id': id,
        'count': range(datas.count()),
    }

    return render(request, 'csm_add_quizz.html', context)

def csmDeleteQues(request,delId,w_id):
    print(w_id)
    print(delId)
    data = Quizz.objects.get(id = delId)
    data.delete()

    messages.success(request,
                     "Question deleted")
    return redirect('csmAddQuizz',w_id)

