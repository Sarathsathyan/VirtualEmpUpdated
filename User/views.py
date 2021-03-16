from django.shortcuts import render,redirect
from django.contrib import messages
import datetime
import uuid
from datetime import timezone
from Admin.models import (UserDetails,CareerCategory,SubCategory,CategoryCourse,RoleDetail,Reference,CareerCategory,SubCategory,CategoryCourse)
from CSM.models import (Course,CreateCourse,Week,Week_Unit,Quizz)
from Blog.models import (BlogManager,BlogHeight,BlogCategory)
from Admin.models import CareerCategory,SubCategory,CategoryCourse,UsedLicense,AdminLicense
from .models import UserContact,UserEducation,UserWorkExperience,UserSkill,CareerChoice,userProgress, Score, userPrice
from CSM.models import Quizz,Result
from CSM.models import Quizz,Result
import re
from moviepy.editor import VideoFileClip
# Create your views here.
from django import template

register = template.Library()
# CSM

def userCfp(request):
    if request.user.is_active:
        user = request.user
        print(user.pk)
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
                user_id=UserDetails.objects.get(user_id=user.pk)
                print(data1.pk, data2.pk, data3.pk)
                #data = CareerChoice(cat_id_id=data1.pk, sub_id_id=data2.pk, cfp_id_id=data3.pk, user_id_id=user.pk)
                data = CareerChoice(cat_id_id=data1.pk, sub_id_id=data2.pk, cfp_id_id=data3.pk, user_id_id=user_id.pk)
                data.save()
                messages.success(request, "CFP choosed")
                details.user_cfp = True
                details.save()
                #return redirect('userdashboard')
                """
                weeks=Week.objects.all()

                for week in weeks:
                    score_ob=Score.objects.create(userId_id=request.user.id, week_id_id=week.pk, totalxp=0)
                    score_ob.save()
                """
                return redirect('userprofileedit')
        career_list = CareerCategory.objects.all()

        context = {
            'career_list': career_list,
            'sub_cats': sub_cats,
            's_courses': s_courses,
            'data': data,
            's_data': s_data,
            'c_data': c_data,
            'worktokens':details.user_workTokens,
            'mcCredits':details.user_mcCredits
        }
        return render(request, 'userCFP.html', context)
    else:
        return redirect('login')

def userDashboard(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        print("request.user.pk form dashboard", user.pk)
        #user_details = UserDetails.objects.get(user_id_id=user.pk)
        #allData = CareerChoice.objects.get(user_id_id=user.pk)
        user_details = UserDetails.objects.get(user_id=user.pk)
        allData = CareerChoice.objects.get(user_id_id=user_details.id)

        category = allData.cat_id
        sub = allData.sub_id
        cour = allData.cfp_id
        if CreateCourse.objects.get(create_category=category,create_sub=sub,create_course=cour):
            createCourse = CreateCourse.objects.get(create_category=category,create_sub=sub,create_course=cour)
        else:
            createCourse = None
            messages.error(request,"Please choose CFP")
            return redirect('usercfp')
        #careerChoice = CareerChoice.objects.get(user_id_id=request.user.pk)
        careerChoice = CareerChoice.objects.get(user_id_id=user_details.id)
        print(careerChoice.cat_id_id)

        # Blogs
        blog_cag = BlogCategory.objects.all()
        blogs = BlogManager.objects.all()
        if not blogs:
            blogs = BlogHeight.objects.all()
        course = Course.objects.get(category_id=createCourse.pk)
        print(course.title)
        print("user_details.user_mcCredits",user_details.user_mcCredits)
        context={
            'careerChoice' :careerChoice,
            'course':course,
            'blog_cag': blog_cag,
            'blogs': blogs,
            'cour':cour,
            'mcCredits':user_details.user_mcCredits,
            'worktokens':user_details.user_workTokens
        }
        return render(request,'userDashboard.html',context)
    else:
        print("Wrong url")
        return redirect('login')

# user course
def userCourseIntro(request,course_id):
    if request.user.is_active:
        course=Course.objects.get(id=course_id)
        user_details = UserDetails.objects.get(user_id=request.user.pk)
        if course:
            short_desp=course.short_description
            f_req, s_req, l_req =re.split("_",course.requirements)
            req_list=[f_req, s_req, l_req]
            print(len(req_list))
            f_learn, s_learn, l_learn =re.split("_",course.learnings)
            learn_list=[f_learn, s_learn, l_learn]
            print(len(req_list))
            topics=Week_Unit.objects.all()
            clip_duration=0
            sec=0
            min=0
            hr=0
            for topic in topics:
                if topic.video1_duration:
                    sec+= topic.video1_duration.second
                    min+= topic.video1_duration.minute
                    hr+=topic.video1_duration.hour
                if topic.video2_duration:
                    sec+= topic.video2_duration.second
                    min+= topic.video2_duration.minute
                    hr+=topic.video2_duration.hour
                if topic.video2_duration:
                    sec+= topic.video3_duration.second
                    min+= topic.video3_duration.minute
                    hr+=topic.video3_duration.hour
            hr=sec//3600
            sec%=3600
            min=sec//60
            sec%=60
            context ={
                'course_id':course_id,
                'course_details':course,
                'short_desp':short_desp,
                'req_list':[i for i in req_list if i],
                'learn_list': [i for i in learn_list if i],
                'lessons': Week.objects.all(),
                 #'lessons': Week.objects.order_by("week_name"),
                'topics':topics,
                'course_duration_hr':hr,
                'course_duration_min':min,
                'course_duration_sec':sec,
                'mcCredits':user_details.user_mcCredits,
                'worktokens':user_details.user_workTokens
            }
            for topic in Week_Unit.objects.all():
                print(topic.video1_duration)
            return render(request,'userCourseIntro.html',context)


        course = Course.objects.get(id=course_id)
        week = Week.objects.filter(week_id_id=course.pk)

        context ={
            'course_id':course_id,
            'week':week,
            'mcCredits':user_details.user_mcCredits,
            'worktokens':user_details.user_workTokens
        }
        return render(request,'userCourseIntro.html',context)
    else:
        return redirect('login')

def userCourseLesson(request, c_id):
    if request.user.is_active:
        user_details = UserDetails.objects.get(user_id=request.user.pk)
        current_time = datetime.datetime.now(timezone.utc)
        print(c_id)
        # give c_id in 1
        course = Course.objects.get(id=c_id)
        data = userProgress.objects.filter(userId_id=request.user.pk)

        video =None
        week = Week.objects.filter(week_id_id=course.pk)
        weekUnit = Week_Unit.objects.all()
        status=None
        # start test
        testID = False

        if request.method == 'POST':
            if 'start' in request.POST:
                week = request.POST['weekId']

                if userProgress.objects.filter(userId_id=request.user.pk, weekId_id=week).exists():
                    status = 1
                    print(status)
                    print("sarath")
                else:
                    current_time = datetime.datetime.now()
                    end_date = current_time + datetime.timedelta(days=7)
                    data = userProgress(weekId_id=week,userId_id=request.user.pk,course_id_id=course.pk,status='STARTED',currentTime=current_time,endTime=end_date)
                    data.save()
                return redirect('courseLesson',c_id)
            if 'videoOne' in request.POST:
                key = request.POST['uniq']
                video = Week_Unit.objects.get(id =key)
                video = video.unit_video1
            if 'videoTwo' in request.POST:
                twoKey = request.POST['uniq']
                video = Week_Unit.objects.get(id=twoKey)
                video = video.unit_video2
            if 'videoThree' in request.POST:
                threeKey = request.POST['uniq']
                video = Week_Unit.objects.get(id=threeKey)
                video = video.unit_video3
        remainingTime = 7
        for i in week:
            for d in data:
                if(d.weekId_id == i.pk):
                    if(d.endTime):
                        remainingTime = d.endTime - current_time

                        if remainingTime.days == 0:
                            testID = True

        if course.video_page_image == None:
            video_page_image= None
        else:
            video_page_image= course.video_page_image


        context ={
            'week':week,
            'weekUnits':weekUnit,
            'video':video,
            'data':data,
            'status':status,
            'remain':remainingTime,
            'video_page_image':video_page_image,
            'mcCredits':user_details.user_mcCredits,
            'worktokens':user_details.user_workTokens,
            'testCheck':testID

        }
        return render(request,'userCourseLesson.html',context)
    else:
        return redirect('login')



def userprofile(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        user_details = UserDetails.objects.get(user_id_id=user.pk)
        user_education=None
        #score_ob=score.objects.filter(userId_id=user.pk)

        #print(score_ob)

        if UserEducation.objects.filter(user_id_id=user_details.pk).exists():
            user_education = UserEducation.objects.filter(user_id_id=user_details.pk)
            try:
                work = UserWorkExperience.objects.filter(user_id_id=user_details.pk).order_by("-start_year")
            except:
                work=[]

            try:
                tech_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Technical')
            except:
                tech_skills=[]

            try:
                man_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Management')
            except:
                man_skills=[]

            try:
                lan_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Languages')
            except:
                lan_skills=[]



            context = {
                'user_education':user_education,
                'user_data': user_details,
                'work': work,
                'tech_skills':tech_skills,
                'man_skills':man_skills,
                'lan_skills':lan_skills,
                'mcCredits':user_details.user_mcCredits,
                'worktokens':user_details.user_workTokens,
                'numberCfp':user_details.numberCfp
                #'cfp_name':cfp_name
            }
            if UserContact.objects.filter(user_id_id=user_details.pk).exists():
                user_contact = UserContact.objects.get(user_id_id=user_details.pk)
                try:
                    work = UserWorkExperience.objects.filter(user_id_id=user_details.pk).order_by("-start_year")
                except:
                    work=[]


                try:
                    tech_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Technical')
                except:
                    tech_skills=[]

                try:
                    man_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Management')
                except:
                    man_skills=[]

                try:
                    lan_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Languages')
                except:
                    lan_skills=[]

                    # Certificate Retrieval


                context={
                    'user_contact':user_contact,
                    'user_education': user_education,
                    'user_data': user_details,
                    'work':work,
                    'tech_skills':tech_skills,
                    'man_skills':man_skills,
                    'lan_skills':lan_skills,
                    'mcCredits':user_details.user_mcCredits,
                    'worktokens':user_details.user_workTokens,
                    'numberCfp':user_details.numberCfp
                    #'cfp_name':cfp_name


                }

                #if CareerChoice.objects.filter(user_id_id=user_details.pk).exists():
                if CareerChoice.objects.filter(user_id_id=user_details.pk).exists():
                    print("")
                    cfp_details = CareerChoice.objects.get(user_id_id=user_details.pk)
                    cfp_name=cfp_details.cfp_id.cfp

                    # CFP  COURSES
                    #lists = Course.objects.filter(category=cfp_details.category_one, role=cfp_details.role_one)
                    #lists2 = Course.objects.filter(category=cfp_details.category_two, role=cfp_details.role_two)
                    try:
                        work = UserWorkExperience.objects.filter(user_id_id=user_details.pk).order_by("-start_year")
                    except:
                        work=[]

                    try:
                        tech_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Technical')
                    except:
                        tech_skills=[]

                    try:
                        man_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Management')
                    except:
                        man_skills=[]

                    try:
                        lan_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Languages')
                    except:
                        lan_skills=[]
                    print("request.user.pk")
                    print(request.user.pk)

                    if Score.objects.filter(userId_id=request.user.pk).exists():
                        score_ob=Score.objects.filter(userId_id=request.user.pk)
                        total_xp_earned=0

                        for score in score_ob:
                            total_xp_earned+=score.totalxp
                            print("total_xp_earned:")

                            course_points=Course.objects.get(id=score.week_id.week_id_id).course_points


                    else:
                        total_xp_earned=0
                        course_points=0

                    context = {
                        'cfp_details': cfp_details,
                        'user_data': user_details,
                        'user_contact': user_contact,
                        'user_education': user_education,
                        'work':work,
                        'tech_skills':tech_skills,
                        'man_skills':man_skills,
                        'lan_skills':lan_skills,
                        'cfp_name':cfp_name,
                        'total_xp_earned':total_xp_earned,
                        'course_points':course_points,
                        'mcCredits':user_details.user_mcCredits,
                        'worktokens':user_details.user_workTokens,
                        'numberCfp':user_details.numberCfp,
                        #'course_perc':(total_xp_earned/1000)*100
                    }
                    return render(request, "userProfile.html", context)
                return render(request, "userProfile.html", context)
            return render(request,"userProfile.html",context)
        context = {
            'user_data' : user_details,
            'mcCredits':user_details.user_mcCredits,
            'worktokens':user_details.user_workTokens,
            'numberCfp':user_details.numberCfp
            #'cfp_name':cfp_name
        }
        return render(request,"userProfile.html",context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')


def userProfileEdit(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:

        user = request.user
        user_detail = UserDetails.objects.get(user_id_id=user.id)
        # print(user_detail.pk)
        if request.method == 'POST':

            if 'contact' in request.POST:
                if UserContact.objects.filter(user_id_id=user_detail.pk).exists():
                    address1 = request.POST['address1']
                    address2 = request.POST['address2']
                    gender = request.POST['gender']
                    bio=request.POST['bio']
                    data = UserContact.objects.get(user_id_id=user_detail.pk)
                    data.address1 = address1
                    data.address2 = address2
                    data.gender = gender
                    data.user_bio=bio
                    data.save()
                    messages.success(request,"Updated Contact Info")
                    return redirect('userprofileedit')

                else:
                    address1 = request.POST['address1']
                    address2 = request.POST['address2']
                    gender = request.POST['gender']
                    bio=request.POST['bio']
                    data = UserContact(address1=address1,address2=address2,gender=gender,user_bio=bio,user_id_id=user_detail.pk)
                    data.save()
                    messages.success(request,"Contact Info added")
                    return redirect('userprofileedit')
            if 'photo' in request.POST:
                try:
                    data = UserContact.objects.get(user_id_id=user_detail.pk)
                    if data.user_pic:
                        pic = request.FILES.get('user-profile-photo')
                        print(pic)
                        print("hai")
                        data.user_pic = pic
                        data.save()
                        messages.success(request,"Profile pic updated")
                    else:
                        pic = request.FILES.get('user-profile-photo')
                        certi_create=request.POST['certi_create']
                        data.user_pic = pic
                        data.save()

                        messages.success(request, "Profile pic added")
                except:
                    messages.error(request,"Complete your contact info to change Pic")
                    return redirect("userProfileEdit")


            if 'skill' in request.POST:
                type=request.POST['type']
                skills=request.POST['skills']

                create=UserSkill(user_id_id=user_detail.pk,category=type,skill=skills)
                create.save()
                messages.success(request, "Skills Added")

                return redirect(request.path_info)

            if 'tech_del' in request.POST:
                type=request.POST['type']
                skill=request.POST['skill1']

                find=UserSkill.objects.filter(user_id_id=user_detail.pk,category=type,skill=skill) #previously get()
                find.delete()
                messages.success(request,"Technical Skill Deleted")
                return redirect(request.path_info)

            if 'man_del' in request.POST:
                type=request.POST['type']
                skill=request.POST['skill2']

                find=UserSkill.objects.filter(user_id_id=user_detail.pk,category=type,skill=skill)
                find.delete()
                messages.success(request,"Management Skill Deleted")
                return redirect(request.path_info)

            if 'lan_del' in request.POST:
                type=request.POST['type']
                skill=request.POST['skill3']

                find=UserSkill.objects.filter(user_id_id=user_detail.pk,category=type,skill=skill)
                find.delete()
                messages.success(request,"Language Deleted")
                return redirect(request.path_info)



            if 'education' in request.POST:
                institution=request.POST['institution']
                start_month=request.POST['start-month']
                start_year=request.POST['start-year']
                end_month=request.POST['end-month']
                end_year=request.POST['end-year']
                degree=request.POST['degree']
                special=request.POST['special']
                gpa=request.POST['gpa']
                state=request.POST['state']


                if(start_month== 'Jan'):
                    x=1;
                elif(start_month== 'Feb'):
                    x=2;
                elif(start_month== 'Mar'):
                    x=3;
                elif(start_month== 'Apr'):
                    x=4;
                elif(start_month== 'May'):
                    x=5;
                elif(start_month== 'Jun'):
                    x=6;
                elif(start_month== 'Jul'):
                    x=7;
                elif(start_month== 'Aug'):
                    x=8;
                elif(start_month== 'Sept'):
                    x=9;
                elif(start_month== 'Oct'):
                    x=10;
                elif(start_month== 'Nov'):
                    x=11;
                elif(start_month== 'Dec'):
                    x=12;


                if(end_month== 'Jan'):
                    y=1;
                elif(end_month== 'Feb'):
                    y=2;
                elif(end_month== 'Mar'):
                    y=3;
                elif(end_month== 'Apr'):
                    y=4;
                elif(end_month== 'May'):
                    y=5;
                elif(end_month== 'Jun'):
                    y=6;
                elif(end_month== 'Jul'):
                    y=7;
                elif(end_month== 'Aug'):
                    y=8;
                elif(end_month== 'Sept'):
                    y=9;
                elif(end_month== 'Oct'):
                    y=10;
                elif(end_month== 'Nov'):
                    y=11;
                elif(end_month== 'Dec'):
                    y=12;
                num_months = (int(end_year) - int(start_year)) * 12 + (y - x)

                num_years=int(num_months/12)
                num_months=num_months%12
                durr=str(num_years)+ "y " + str(num_months) + "m"
                edu=UserEducation(user_id_id=user_detail.pk,institution=institution,start_month=start_month,start_year=start_year,end_month=end_month,end_year=end_year,state=state,degree=degree,specialization=special,gpa=gpa)
                edu.save()
                messages.success(request, "Updated Education Info")
                return redirect(request.path_info)


            if 'work' in request.POST:
                role=request.POST['role']
                start_month=request.POST['start-month']
                start_year=request.POST['start-year']
                end_month=request.POST['end-month']
                end_year=request.POST['end-year']
                company=request.POST['company']
                state=request.POST['state']
                if(start_month== 'Jan'):
                    x=1;
                elif(start_month== 'Feb'):
                    x=2;
                elif(start_month== 'Mar'):
                    x=3;
                elif(start_month== 'Apr'):
                    x=4;
                elif(start_month== 'May'):
                    x=5;
                elif(start_month== 'Jun'):
                    x=6;
                elif(start_month== 'Jul'):
                    x=7;
                elif(start_month== 'Aug'):
                    x=8;
                elif(start_month== 'Sept'):
                    x=9;
                elif(start_month== 'Oct'):
                    x=10;
                elif(start_month== 'Nov'):
                    x=11;
                elif(start_month== 'Dec'):
                    x=12;


                if(end_month== 'Jan'):
                    y=1;
                elif(end_month== 'Feb'):
                    y=2;
                elif(end_month== 'Mar'):
                    y=3;
                elif(end_month== 'Apr'):
                    y=4;
                elif(end_month== 'May'):
                    y=5;
                elif(end_month== 'Jun'):
                    y=6;
                elif(end_month== 'Jul'):
                    y=7;
                elif(end_month== 'Aug'):
                    y=8;
                elif(end_month== 'Sept'):
                    y=9;
                elif(end_month== 'Oct'):
                    y=10;
                elif(end_month== 'Nov'):
                    y=11;
                elif(end_month== 'Dec'):
                    y=12;


                num_months = (int(end_year) - int(start_year)) * 12 + (y - x)

                num_years=int(num_months/12)
                num_months=num_months%12
                durr=str(num_years)+ "y " + str(num_months) + "m"


                work=UserWorkExperience(user_id_id=user_detail.pk,job_role=role,start_month=start_month,start_year=start_year,end_month=end_month,end_year=end_year,state=state,company=company)
                work.save()

                messages.success(request, "Work Experience Added")
                return redirect(request.path_info)


            if 'edu_del' in request.POST:
                deg=request.POST['deg']
                spec=request.POST['spec']
                ins=request.POST['ins']

                find=UserEducation.objects.get(user_id_id=user_detail.pk,degree=deg,specialization=spec,institution=ins)
                find.delete()

                messages.success(request,"Educational Details Deleted")
                return redirect(request.path_info)

            if 'work_del' in request.POST:
                role=request.POST['role']
                com=request.POST['com']
                sm=request.POST['sm']
                sy=request.POST['sy']

                find=UserWorkExperience.objects.get(user_id_id=user_detail.pk,job_role=role,company=com,start_month=sm,start_year=sy)
                find.delete()

                messages.success(request,"Work Experience Deleted")
                return redirect(request.path_info)


        if UserContact.objects.filter(user_id_id=user_detail.pk).exists():

            users = UserContact.objects.order_by("gender")

            context ={
                'user_detail' : user_detail,
                'users' : users,
                'mcCredits':user_detail.user_mcCredits,
                'worktokens':user_detail.user_workTokens,

            }

            try:
                work=UserWorkExperience.objects.filter(user_id_id=user_detail.pk).order_by("-start_year")
            except:
                work=[]

            try:
                tech_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Technical')
            except:
                tech_skills=[]

            try:
                man_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Management')
            except:
                man_skills=[]

            try:
                lan_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Languages')
            except:
                lan_skills=[]


            if UserEducation.objects.filter(user_id_id=user_detail.pk).exists():

                try:
                    work=UserWorkExperience.objects.filter(user_id_id=user_detail.pk).order_by("-start_year")
                except:
                    work=[]

                try:
                    tech_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Technical')
                except:
                    tech_skills=[]

                try:
                    man_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Management')
                except:
                    man_skills=[]

                try:
                    lan_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Languages')
                except:
                    lan_skills=[]

                users = UserContact.objects.order_by("gender")
                education = UserEducation.objects.filter(user_id_id=user_detail.pk)
                context = {
                    'user_detail': user_detail,
                    'users': users,
                    'education': education,
                    'work':work,
                    'tech_skills':tech_skills,
                    'man_skills':man_skills,
                    'lan_skills':lan_skills,
                    'mcCredits':user_detail.user_mcCredits,
                    'worktokens':user_detail.user_workTokens

                }

                return render(request,'userProfileEdit.html',context)
            else:
                context ={
                    'work':work,
                    'tech_skills':tech_skills,
                    'man_skills':man_skills,
                    'lan_skills':lan_skills,
                    'user_detail': user_detail,
                    'users': users,
                    "edd":1,
                    'mcCredits':user_detail.user_mcCredits,
                    'worktokens':user_detail.user_workTokens
                }
                return render(request,'userProfileEdit.html',context)
            return render(request,'userProfileEdit.html',context)
        else:
            context={
                "idd":1,
                "edd":1,
                'user_detail':user_detail,
                'mcCredits':user_detail.user_mcCredits,
                'worktokens':user_detail.user_workTokens
            }
            idd =1
            return render(request,'userProfileEdit.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')


def userQuizz(request,w_id):
    if request.user.is_active:
        week = Week.objects.get(id = w_id)
        course = Course.objects.get(id = week.week_id_id)

        if not Score.objects.filter(userId_id=request.user.pk, week_id_id=week.pk).exists():
            score_ob=Score.objects.create(userId_id=request.user.id,week_id_id=week.pk, totalxp=0)
            score_ob.save()

        data = Quizz.objects.filter(course_id_id=course.pk, week_id_id = week.pk)

        context={
            'questions' : data,
            'w_id':w_id
        }
        return render(request,'userQuizz.html',context)
    else:
        return redirect('login')


def userResult(request,w_id):
    if request.user.is_active:
        time =0
        form = request.POST.getlist('inquiry')
        print(form)
        correct = 0
        wrong = 0
        tempQues = []
        tempRes = []
        dic_quizz={}
        for i in form:
            print("i",i)
            if i in request.POST:
                ques = request.POST[i]
                tempQues.append(ques)
                Ques = Quizz.objects.filter(id=i)
                #Ques = Quizz.objects.get(id=i)
                dic_quizz[Ques[0].week_id_id]=0
                print(Ques[0].week_id_id)
                print("Ques",Ques)
                res = Ques[0].answer
                tempRes.append(res)
                if (res == ques):
                    correct += 1
                    #dic_quizz[Ques[0].week_id_id]+=1
                    #dic_quizz[Ques[0].week_id_id]=correct
                else:
                    wrong += 1

        val = Result()
        print("correct",correct)
        print("Wrong",wrong)
        dic_quizz[Ques[0].week_id_id]=correct
        """
        # obj = Question.objects.first()
        # field_value = getattr(obj,'title')
        # print ("************************************")
        # print(field_value)
        # print ("************************************")
        val.result = [{'questions': form, 'user_answers': tempQues}]
        val.score = str(correct) + '/' + str(20)
        # val.timetaken = str(time)
        val.user_answer = [{'user_answers': tempQues, 'correct_answer': tempRes}]
        val.auth_id = (request.user.id)
        val.save()
        print("val",val)
        """
        #score_ob=score.objects.filter(userId_id=request.user.id)
        print("dic_quizz",dic_quizz)
        for k in dic_quizz.keys():
            if Score.objects.filter(week_id_id=k, userId_id=request.user.id).exists():
                score_ob=Score.objects.get(week_id_id=k, userId_id= request.user.id)
                score_ob.correct = correct
                score_ob.wrong = wrong
                score_ob.save()
                course_ob=Course.objects.get(id=score_ob.week_id.week_id_id)
                temp_totalxp=dic_quizz[k] * course_ob.xp_points_perq
                if temp_totalxp > score_ob.totalxp:
                    score_ob.totalxp=temp_totalxp
                    score_ob.save()

        print(len(form))
        context ={
            'total' : len(form),
            'correct' : correct,
            'wrong' : wrong,
            'w_id':w_id
        }

        return render(request,'user_result.html',context)

        # except Exception as e:
        #     messages.add_message(
        #             request,
        #             messages.INFO,
        #             e
        #         )
        #     return redirect('/')
    else:
        return redirect('login')


def userProjects(request):
    blog_cag = BlogCategory.objects.all()
    blogs = BlogManager.objects.all()
    if not blogs:
        blogs = BlogHeight.objects.all()

    context={
        'blog_cag': blog_cag,
        'blogs': blogs,
    }
    return render(request,'userProject.html',context)


def userProjectsDesc(request):

    return render(request,'userProjectDesc.html')

def unlock(request,w_id):
    user_id = request.user.pk
    week = Week.objects.get(id = w_id)
    next_week = None
    data=None
    if userProgress.objects.filter(userId_id=user_id , weekId_id = week.pk).exists():
        data = userProgress.objects.get(userId_id=user_id , weekId_id = week.pk)
        print(data.course_id)

    if(week.week_name == 'Week 1'):
        next_week = 'Week 2'
        week_data = Week.objects.get(week_name=next_week)
        print(week_data.week_name)
        current_time = datetime.datetime.now()
        end_date = current_time + datetime.timedelta(days=7)
        next = userProgress(weekId_id=week_data.pk, userId_id=request.user.pk,course_id_id=data.course_id_id,status='STARTED',currentTime=current_time,endTime=end_date)
        next.save()
        return redirect('courseLesson',data.course_id_id)





def pricing(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        cefPrice =12000
        cfpPath = 1
        cfpPrice = 3000
        tokenPrice = 3750
        courseCreditPrice = 0
        total =0
        discount =0
        workToken=5
        courseCredits=5
        if 'checkoutSubmit' in request.POST:
            print("checkout  button")
            user_id=request.user.pk
            if 'radio3' in request.POST:
                print("yes")
            workToken = request.POST.get('radio3')
            courseCredits = request.POST.get('mcRadio2')
            if int(workToken) == 5:
                tokenPrice = 3750
            elif int(workToken) == 8:
                tokenPrice =5200
            elif int(workToken) == 15:
                tokenPrice =6000
            else:
                tokenPrice = 0

            if int(courseCredits) == 5:
                courseCreditPrice = 0
            elif int(courseCredits) == 8:
                courseCreditPrice = 1000
            elif int(courseCredits) == 15:
                courseCreditPrice = 1500
            if userPrice.objects.filter(userId_id=user_id).exists():
                print("yes")
                user_data=userPrice.objects.get(userId_id=user_id)
                user_data.tokenPrice=tokenPrice
                user_data.courseCreditPrice=courseCreditPrice
                user_data.workToken=workToken
                user_data.mcCredit=courseCredits
                user_data.save()
                
            else:
                print("no")
                data = userPrice(userId_id=request.user.pk,cfpPrice=cfpPrice,tokenPrice=tokenPrice,courseCreditPrice=courseCreditPrice,totalPrice=total,cefPrice=cefPrice,workToken=workToken,mcCredit=courseCredits)
                data.save()


            return redirect("license_page")
        """
        if 'cSubmit' in request.POST:
            #return redirect("license_page")
            #workToken = request.POST['radio3']
            #courseCredits = request.POST['mcRadio2']
            if int(workToken) == 5:
                tokenPrice = 3750
            elif int(workToken) == 8:
                tokenPrice =5200
            elif int(workToken) == 15:
                tokenPrice =6000
            else:
                tokenPrice = 0

            if int(courseCredits) == 5:
                courseCreditPrice = 0
            elif int(courseCredits) == 8:
                courseCreditPrice = 1000
            elif int(courseCredits) == 15:
                courseCreditPrice = 1500

            print(tokenPrice)
            data = userPrice(userId_id=request.user.pk,cfpPrice=cfpPrice,tokenPrice=tokenPrice,courseCreditPrice=courseCreditPrice,totalPrice=total,cefPrice=cefPrice,workToken=workToken,mcCredit=courseCredits)
            data.save()
        """
        #total = cfpPrice+tokenPrice+courseCreditPrice+cefPrice+courseCreditPrice
        total = cfpPrice+tokenPrice+courseCreditPrice+cefPrice
        total_includ_gst= float(total) *1.18
        discount = int(total_includ_gst) - ((int(total_includ_gst) * 30 ) / 100)
        
        print(total_includ_gst)

        context ={
            'cefPrice' : cefPrice,
            'total':total,
            'total_includ_gst': total_includ_gst,
            'cfpPrice':cfpPrice,
            'tokenPrice':tokenPrice,
            'courseCreditPrice':courseCreditPrice,
            'discount':discount,
            'wtokens':5,
            'mccred':5,

        }
        return render(request,'pricing.html',context)
        
    else:
        return redirect('login')

def license_generate(request):
    userId = request.user.pk
    data = userPrice.objects.get(userId_id=request.user.pk)
    if data:
        l_id = uuid.uuid4()
        license_key = l_id

        delData = AdminLicense(key=license_key,numberCfp=1,workTokens=data.workToken,mcCredits=data.mcCredit)
        delData.save()
        cfp=1
        worktoken=data.workToken
        mccreddit=data.mcCredit
        context={
            'cfp':cfp,
            'worktoken':worktoken,
            'mccredit': mccreddit,
            'license':license_key
        }
        #return render(request, 'license_generate.html',context)
        return render(request,'license_page.html',context)

    #return render(request,'license_generate.html')
    return render(request,'license_page.html')



def license_page(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user_id=request.user.pk
        if userPrice.objects.filter(userId_id=user_id).exists():
            user_data=userPrice.objects.get(userId_id=user_id)
            cfp=1
            worktoken=user_data.workToken
            mccreddit=user_data.mcCredit
            context={
                'cfp':cfp,
                'worktoken':worktoken,
                'mccredit': mccreddit
            }

        if 'license_button' in request.POST:
            print("activate")
            return  redirect('license_generate')

        """elif 'activate_license_btn' in request.POST:
            print("activate   plz")
            return redirect('activatecode')"""
        return render(request,'license_page.html',context)
    else:
        return redirect('login')