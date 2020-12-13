import re
import random
from django.shortcuts import render,redirect
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import auth
# EMAIL FROM SETTINGS
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from VirtualEmpleado.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage
from .forms import (AddUserForm)
from .models import UserDetails,Reference,RoleDetail,CareerCategory,SubCategory,CategoryCourse
# Create your views here.

def landing(request):
    return render(request, 'landing.html')

def user_logout(request):
    auth.logout(request)
    return render(request, 'logout.html')

def userLogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        # Roles
        if user is not None:
            login(request, user)
            if request.user.is_staff and request.user.is_superuser:
                print('Welcome admin')
                return redirect('admindashboard')
            else:
                try:
                    print("user role")
                    if RoleDetail.objects.filter(role_user_email=email).exists():
                        print("user role")
                        role = RoleDetail.objects.get(role_user_email=email)
                        if role.user_role == "CSM":
                            return redirect('csmDashboard/')
                        elif role.user_role == "TL":
                            return redirect('tlDashboard')
                        elif role.user_role == "PCM":
                            return redirect('projectDashboard')
                        elif role.user_role == "Instructor":
                            return redirect('insDashboard')
                        elif role.user_role == "Blogger":
                            return redirect('blogManager')
                        else:
                            messages.error(request, "Error occured in Role")
                except:
                    messages.error(request, "login failed")
                    print("error testing check")
                if request.user.is_active:
                    try:
                        license = UserDetails.objects.get(user_id_id=user.pk)
                        if license.user_license:
                            print("license key added")
                        else:
                            print("No license key")
                            # messages.success(request, "Apply License Key")
                            # return redirect('activatecode')
                    except:
                        messages.error(request, "Dont have permission to login")
                        return redirect('login')
                    try:
                        user_cfp = UserDetails.objects.get(user_id_id=user.pk)
                        print(user_cfp.user_cfp)
                        print("helloooo")
                        if user_cfp.user_cfp == False:
                            user_cfp.user_cfp = True
                            user_cfp.save()
                            messages.success(request, "Choose your career focus path ! Enjoy")
                            return redirect('usercfp')
                        else:
                            return redirect('userdashboard/')
                    except:
                        user_cfp = UserDetails.objects.get(user_id_id=user.pk)
                        user_cfp.user_cfp = True
                    return redirect('userdashboard/')
        messages.error(request, "Login failed")
        return redirect('login')
    return render(request,'login.html')

def userRegister(request):
    form = AddUserForm
    if request.method == 'POST':
        firstname = request.POST['first']
        lastname = request.POST['last']
        userphone = request.POST['user_phone']
        email = request.POST['email']
        username = request.POST['email']
        password = request.POST['password1']
        conform = request.POST['password2']
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'That email is being used')
            return redirect('register')
        if firstname.isdigit():
            messages.error(request, 'Firstname cannot have numbers')
            return redirect('register')
        if lastname.isdigit():
            messages.error(request, 'Lastname cannot have numbers')
            return redirect('register')
        if regex.search(firstname):
            messages.error(request, 'firstname cannot have special characters')
            return redirect('register')
        if regex.search(lastname):
            messages.error(request, 'lastname cannot have special characters')
            return redirect('register')
        try:
            v = validate_email(email)
            val_email = v["email"]
        except EmailNotValidError as e:
            messages.error(request, 'Invalid Email ID')
            return redirect('register')
        if password != conform:
            messages.error(request, 'Password mismatch')
            return redirect('register')
        num = random.randint(10000000, 99999999)
        str1 = 'VE'
        unique_id = str1 + str(num)
        # Generating reference id
        ref = random.randint(54866, 9854721)
        str2 = firstname
        reference_id = str2 + str(ref)
        try:
            license_key = None
            User.objects.create_user(username=username, email=email, first_name=firstname, last_name=lastname,
                                     password=password)
            u_id = User.objects.get(username=username)
            addusr = UserDetails(user_id=u_id, user_pass=password, user_phone=userphone, user_unique=unique_id,
                                 user_license=license_key)
            addusr.save()
            ref_user = Reference(user_id=u_id, ref_id=reference_id, used_peoples=None, used_id=None)
            ref_user.save()
        except:
            usr = User.objects.get(username=email)
            usr.delete()
            messages.error(request, 'Some error occured !')
            return redirect('register')
        messages.success(request, 'User Added!')
        return redirect('login')
    context = {
        'form': form
    }
    return render(request,'register.html',context)

def adminDashboard(request):
    return render(request,'dashboard.html')

def roleCreation(request):
    if request.user.is_staff and request.user.is_superuser:
        if request.method == 'POST':
            # When we Press Create Role Button
            if 'create' in request.POST:
                # Assigning Unique Id To each role
                user_role = request.POST['role']
                if user_role == "CSM":
                    role_user_id = "CM" + str(100 + (RoleDetail.objects.filter(user_role="CSM").count() + 1))
                elif user_role == "PCM":
                    role_user_id = "PM" + str(200 + (RoleDetail.objects.filter(user_role="PCM").count() + 1))
                elif user_role == "TL":
                    role_user_id = "TL" + str(300 + (RoleDetail.objects.filter(user_role="TL").count() + 1))
                elif user_role == "Instructor":
                    role_user_id = "IN" + str(400 + (RoleDetail.objects.filter(user_role="Instructor").count() + 1))
                elif user_role == "Blogger":
                    role_user_id = "Blog" + str(500 + (RoleDetail.objects.filter(user_role="Blogger").count() + 1))
                elif user_role == "Micro Course":
                    role_user_id = "Micro" + str(
                        500 + (RoleDetail.objects.filter(user_role="Micro Course").count() + 1))
                else:
                    role_user_id = 000

                user_firstname = request.POST['fname']
                user_lastname = request.POST['lname']
                role_user_name = request.POST['email']
                role_user_email = request.POST['email']
                regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                if User.objects.filter(email=role_user_email).exists():
                    messages.error(request, 'The email already exists')
                    return redirect('adminrolecreation')
                if User.objects.filter(username=role_user_name).exists():
                    messages.error(request, 'That username is being used')
                    return redirect('adminrolecreation')
                if user_firstname.isdigit():
                    messages.error(request, 'Firstname cannot have numbers')
                    return redirect('adminrolecreation')
                if regex.search(user_firstname):
                    messages.error(request, 'Firstname cannot have special characters')
                    return redirect('adminrolecreation')
                if user_lastname.isdigit():
                    messages.error(request, 'Lastname cannot have numbers')
                    return redirect('adminrolecreation')
                if regex.search(user_lastname):
                    messages.error(request, 'Lastname cannot have special characters')
                    return redirect('adminrolecreation')

                role_user_password = request.POST['password']
                mail_subject = "[Activate Account] VE - Virtual Employee"
                current_site = get_current_site(request)
                message = render_to_string('user_info.html', {
                    'user': role_user_email,
                    'firstname': user_firstname,
                    'lastname': user_lastname,
                    'domain': current_site.domain,
                    'pass': role_user_password,
                })
                email = EmailMessage(mail_subject, message, from_email=EMAIL_HOST_USER, to=[role_user_email])
                email.send()
                try:

                    user = User.objects.create_user(username=role_user_name, email=role_user_email,
                                                    first_name=user_firstname,
                                                    last_name=user_lastname, password=role_user_password)
                    if user_role == "CSM":
                        user.is_staff = True
                    elif user_role == "TL":
                        user.is_staff = False
                        user.is_superuser = True
                    elif user_role == "Blogger":
                        user.is_active = True
                        user.is_staff = False
                        user.is_superuser = False
                    elif user_role == "PCM":
                        user.is_superuser = True
                        user.is_staff = False
                    elif user_role == "Micro Course":
                        user.is_superuser = False
                        user.is_staff = False
                    user.save()
                    u_id = User.objects.get(username=role_user_name)
                    role = RoleDetail(user_id=u_id, role_user_id=role_user_id, user_role=user_role,
                                      role_user_name=role_user_name,
                                      role_user_email=role_user_email, role_user_password=role_user_password)
                    role.save()

                except:
                    messages.error(request, "Some error occured")
                    return redirect("rolecreation")
                # Saving the role input in the model
                messages.success(request, "Email has been sent successfully")
                return redirect("rolecreation")

            # When we press Remove Button
            if 'delete' in request.POST:
                del_id = request.POST['del_id']

                if RoleDetail.objects.filter(role_user_id=del_id).exists():
                    main_id_1 = RoleDetail.objects.get(role_user_id=del_id)
                    main_id = main_id_1.user_id_id
                    roled = RoleDetail.objects.get(role_user_id=del_id).delete()
                    # Delete from the user table
                    user_del = User.objects.get(id=main_id).delete()
                    messages.success(request, "Deleted success")
                else:
                    messages.error(request, "Some error occured")
                return redirect('adminrolecreation')

            if 'roleSort' in request.POST:
                role = request.POST['roleSort']
                if role == 'ALL':
                    roled = RoleDetail.objects.all()
                else:
                    roled = RoleDetail.objects.filter(user_role=role)

                context = {
                    'roles': roled
                }
                return render(request, 'rolecreation.html', context)

        roles = RoleDetail.objects.order_by("-role_create_date")
        context = {
            'roles': roles
        }
        return render(request, 'rolecreation.html', context)
    else:
        messages.error(request, "Wrong URL")
        return redirect('logout')
    return render(request,"rolecreation.html")

def cfpCreation(request):
    i=None
    sub = None
    category = None
    if request.method == 'POST':
        if 'category_submit' in request.POST:
            cag_name = request.POST['cagname']
            if CareerCategory.objects.filter(category=cag_name).exists():
                messages.error(request, 'The Category already exists')
                return redirect('cfp_create')

            if CareerCategory.objects.filter(category=cag_name.upper()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('cfp_create')

            if CareerCategory.objects.filter(category=cag_name.lower()).exists():
                messages.error(request, 'The Category admin_pages/cfp_create.htmllready exists')
                return redirect('cfp_create')

            if CareerCategory.objects.filter(category=cag_name.capitalize()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('cfp_create')

            category_id = CareerCategory.objects.all().count() + 1
            cag_obj = CareerCategory(category_id=category_id, category=cag_name)
            cag_obj.save()
            messages.success(request,'Category created')

            return redirect('cfpcreation')

        if 'sub_category' in request.POST:
            category = request.POST['cfp_cag']
            sub_category = request.POST['sub']
            data = CareerCategory.objects.get(category=category)
            print(sub_category)
            cfp_obj = SubCategory(cat_id_id=data.pk, sub_category=sub_category)
            cfp_obj.save()
            messages.success(request, "Sub category created")
            return redirect('cfpcreation')
        if 'career_cat' in request.POST:
            category = request.POST['career_cat']
            i = 1
            career = CareerCategory.objects.get(category=category)
            sub = SubCategory.objects.filter(cat_id_id=career.pk)

        if 'cfp_submit' in request.POST:
            cat = request.POST['career_cat']
            sub_cat = request.POST['cfp_cat']
            cfp_role = request.POST['cfp_role']
            data1 = CareerCategory.objects.get(category=cat)
            data = SubCategory.objects.get(id=sub_cat)
            cfp = CategoryCourse(cat_id_id=data1.pk,sub_id_id=data.pk,cfp=cfp_role)
            cfp.save()
            messages.success(request,
                             'Course cfp created')

        if 'sortlist' in request.POST:
            cfp_category = request.POST['sortlist']
            roles = SubCategory.objects.filter(sub_category=cfp_category)
            category_list = CareerCategory.objects.all()
            context = {
                'category_list': category_list,
                'cfp_list': roles,
            }
            return render(request, 'cfpcreation.html', context)

    category_list = CareerCategory.objects.all()
    cfp_list =SubCategory.objects.all()
    context = {
        'category_list': category_list,
        'cfp_list': cfp_list,
        'i':i,
        'sub':sub,
        'category':category,
    }

    return render(request, 'cfpcreation.html', context)

def cfpList(request):
    return render(request,'cfplist.html')