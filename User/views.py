from django.shortcuts import render,redirect
from django.contrib import messages

from Admin.models import (UserDetails,CareerCategory,SubCategory,CategoryCourse,RoleDetail,Reference,CareerCategory,SubCategory,CategoryCourse)
from .models import UserContact,UserEducation,UserWorkExperience,UserSkill,CareerChoice
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
                # CFP
                # if StudentCFP.objects.filter(user_id_id=user_details.pk).exists():
                #     cfp_details = StudentCFP.objects.get(user_id_id=user_details.pk)
                #     # CFP  COURSES
                #     lists = Course.objects.filter(category=cfp_details.category_one, role=cfp_details.role_one)
                #     lists2 = Course.objects.filter(category=cfp_details.category_two, role=cfp_details.role_two)
                #     try:
                #         work = UserWorkExperience.objects.filter(user_id_id=user_details.pk).order_by("-start_year")
                #     except:
                #         work=[]
                #
                #     try:
                #         tech_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Technical')
                #     except:
                #         tech_skills=[]
                #
                #     try:
                #         man_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Management')
                #     except:
                #         man_skills=[]
                #
                #     try:
                #         lan_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Languages')
                #     except:
                #         lan_skills=[]
                #
                #
                #
                #
                #     context = {
                #         'cfp_details': cfp_details,
                #         'user_data': user_details,
                #         'user_contact': user_contact,
                #         'user_education': user_education,
                #         'work':work,
                #         'tech_skills':tech_skills,
                #         'man_skills':man_skills,
                #         'lan_skills':lan_skills,
                #
                #     }
                #
                #
                #     return render(request, "userProfile.html", context)

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
                    return redirect('userprofileEdit')

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
                    return redirect("userprofileEdit")


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


def userResult(request):
    return render(request,'user_result.html')
