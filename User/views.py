from django.shortcuts import render,redirect
from django.contrib import messages
import datetime
from datetime import timezone
from Admin.models import (UserDetails,CareerCategory,SubCategory,CategoryCourse,RoleDetail,Reference,CareerCategory,SubCategory,CategoryCourse)
from CSM.models import (Course,CreateCourse,Week,Week_Unit,Quizz)
from Blog.models import (BlogManager,BlogHeight,BlogCategory)
from Admin.models import CareerCategory,SubCategory,CategoryCourse,UsedLicense
from .models import UserContact,UserEducation,UserWorkExperience,UserSkill,CareerChoice,userProgress
from CSM.models import Quizz,Result
from CSM.models import Quizz,Result
# Create your views here.

# CSM

def userCfp(request):
    if request.user.is_active:
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
                details.user_cfp = True;
                details.save()
                #return redirect('userdashboard')
                return redirect('userprofileedit')
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
    else:
        return redirect('login')

def userDashboard(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        user_details = UserDetails.objects.get(user_id_id=user.pk)

        # allData = CareerChoice.objects.get(user_id_id=user.pk)

        # category = allData.cat_id
        # sub = allData.sub_id
        # cour = allData.cfp_id
        if CreateCourse.objects.get(create_category=category,create_sub=sub,create_course=cour):
            createCourse = CreateCourse.objects.get(create_category=category,create_sub=sub,create_course=cour)
        else:
            createCourse = None
            messages.error(request,"Please choose CFP")
            return redirect('usercfp')
        careerChoice = CareerChoice.objects.get(user_id_id=request.user.pk)
        print(careerChoice.cat_id_id)

        # Blogs
        blog_cag = BlogCategory.objects.all()
        blogs = BlogManager.objects.all()
        if not blogs:
            blogs = BlogHeight.objects.all()
        course = Course.objects.get(category_id=createCourse.pk)
        print(course.title)
        context={
            'careerChoice' :careerChoice,
            'course':course,
            'blog_cag': blog_cag,
            'blogs': blogs,
            'cour':cour,
        }
        return render(request,'userDashboard.html',context)
    else:
        print("Wrong url")
        return redirect('login')

# user course
def userCourseIntro(request,course_id):
    if request.user.is_active:
        print(course_id)
        course = Course.objects.get(id=course_id)
        week = Week.objects.filter(week_id_id=course.pk)
        context ={
            'course_id':course_id,
            'week':week,
        }
        return render(request,'userCourseIntro.html',context);
    else:
        return redirect('login')

def userCourseLesson(request, c_id):
    if request.user.is_active:
        current_time = datetime.datetime.now(timezone.utc)
        course = Course.objects.get(id=c_id)
        data = userProgress.objects.filter(userId_id=request.user.pk)
        # data.delete()
        video =None;
        week = Week.objects.filter(week_id_id=course.pk)
        weekUnit = Week_Unit.objects.all()
        status=None
        if request.method == 'POST':
            if 'start' in request.POST:
                week = request.POST['weekId']
                if userProgress.objects.filter(userId_id=request.user.pk, weekId_id=week).exists():
                    status = 1
                    print(status)
                else:
                    current_time = datetime.datetime.now()
                    print(current_time)
                    end_date = current_time + datetime.timedelta(days=7)
                    print(end_date)

                    data = userProgress(weekId_id=week,userId_id=request.user.pk,course_id_id=course.pk,status=True,currentTime=current_time,endTime=end_date)
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


        print(status)
        context ={
            'week':week,
            'weekUnits':weekUnit,
            'video':video,
            'data':data,
            'status':status,
            'remain':remainingTime
        }
        return render(request,'userCourseLesson.html',context)
    else:
        return redirect('login')

def userprofile(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        user_details = UserDetails.objects.get(user_id_id=user.pk)
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



                }

                if CareerChoice.objects.filter(user_id_id=user_details.pk).exists():
                    cfp_details = CareerChoice.objects.get(user_id_id=user_details.pk)
                    # CFP  COURSES
                    lists = Course.objects.filter(category=cfp_details.category_one, role=cfp_details.role_one)
                    lists2 = Course.objects.filter(category=cfp_details.category_two, role=cfp_details.role_two)
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
                        'cfp_details': cfp_details,
                        'user_data': user_details,
                        'user_contact': user_contact,
                        'user_education': user_education,
                        'work':work,
                        'tech_skills':tech_skills,
                        'man_skills':man_skills,
                        'lan_skills':lan_skills,

                    }


                    return render(request, "userProfile.html", context)

                return render(request, "userProfile.html", context)

            return render(request,"userProfile.html",context)


        context = {
            'user_data' : user_details,

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
                    'lan_skills':lan_skills

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
                    "edd":1
                }
                return render(request,'userProfileEdit.html',context)
            return render(request,'userProfileEdit.html',context)
        else:
            context={
                "idd":1,
                "edd":1,
                'user_detail':user_detail,


            }
            idd =1
            return render(request,'userProfileEdit.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')


def userQuizz(request,w_id):
    if request.user.is_active:
        week = Week.objects.get(id = w_id);
        course = Course.objects.get(id = week.week_id_id)
        data = Quizz.objects.filter(course_id_id=course.pk, week_id_id = week.pk)

        context={
            'questions' : data
        }
        return render(request,'userQuizz.html',context)
    else:
        return redirect('login')


def userResult(request):
    if request.user.is_active:
        time =0
        form = request.POST.getlist('inquiry')

        correct = 0
        wrong = 0
        tempQues = []
        tempRes = []

        for i in form:
            if i in request.POST:
                ques = request.POST[i]
                tempQues.append(ques)
                Ques = Quizz.objects.filter(id=i)
                res = Ques[0].answer
                tempRes.append(res)
                if (res == ques):
                    correct += 1
                else:
                    wrong += 1

        val = Result()


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
        print(val)
        return redirect('userdashboard')

        # except Exception as e:
        #     messages.add_message(
        #             request,
        #             messages.INFO,
        #             e
        #         )
        #     return redirect('/')
    else:
        return redirect('login')



def pricing(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        cefPrice =12000
        cfpPath = 1
        if 'cSubmit' in request.POST:
            workToken = request.POST['workToken']
            print("hai")


        return render(request,'pricing.html')
    else:
        return redirect('login')        
