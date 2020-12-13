from django.shortcuts import render,redirect
from django.contrib import messages

from Admin.models import (UserDetails,CareerCategory,SubCategory,CategoryCourse,RoleDetail,Reference,CareerCategory,SubCategory,CategoryCourse)
from User.models import UserContact,UserEducation,UserWorkExperience,UserSkill,CareerChoice
from .models import BlogManager,BlogHeight,BlogCategory

def blogManager(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user=request.user
        if request.method=='POST':
            if 'blog_submit' in request.POST:
                blog_title=request.POST["blog_title"]
                blog_tagline=request.POST["blog_tagline"]
                blog_body=request.POST["editor1"]
                blog_thumbnail=request.FILES.get("blog_thumbnail")
                blog_category=request.POST["category"]
                feature=request.POST.get("feature")
                feature = True if feature else False
                if not blog_category:
                    print("no category")


                blog=BlogManager.objects.create(
                    user_id= user.id,
                    blog_title=blog_title,
                    blog_tagline=blog_tagline,
                    blog_body=blog_body,
                    blog_thumbnail=blog_thumbnail,
                    blog_category=blog_category,
                    featured=feature
                )
                # proj.project_cfp.set(cfp_list)
                blog.save()
                return redirect("/blogdashboard/")
        cag_data=BlogCategory.objects.all()
        context={
            'cag_data':cag_data,
        }

        return render(request,'blog_manager.html',context)

    else:
        messages.error(request,"Wrong url")
        return redirect('login')



def blogHighlight(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user= request.user
        if request.method == 'POST':
            if 'blog_submit' in request.POST:
                blog_title = request.POST["blog_title"]
                blog_body = request.POST["blog_body"]
                blog_thumbnail = request.FILES.get("blog_thumbnail")



                blog = BlogHeight.objects.create(
                    user_id=user.id,
                    blog_title=blog_title,
                    blog_body=blog_body,
                    blog_thumbnail=blog_thumbnail,
                )
                # proj.project_cfp.set(cfp_list)
                blog.save()
                return redirect("/blogdashboard/")
        cag_data = BlogHeight.objects.all()
        context = {
            'cag_data': cag_data,
        }
        return render(request, 'blog_highlight.html',context)

    else:
        messages.error(request,"Wrong url")
        return redirect('login')



def blogEditManager(request,id):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user=request.user
        pid=id
        data=BlogManager.objects.get(id=pid)
        cag_data=BlogCategory.objects.all()
        if request.method=='POST':
            if 'blog_edit' in request.POST:
                blog_title=request.POST["blog_title"]
                blog_tagline=request.POST["blog_tagline"]
                blog_body=request.POST["editor1"]
                blog_thumbnail=request.FILES.get("blog_thumbnail")
                blog_category=request.POST["category"]

                data=BlogManager.objects.get(id=pid)
                data.blog_title=blog_title
                data.blog_tagline=blog_tagline
                data.blog_body=blog_body
                data.blog_thumbnail=blog_thumbnail
                data.blog_category=blog_category
                data.save()
                return redirect('blogDashboard')

        context={
            'data':data,
            'cag_data':cag_data
        }

        return render(request,'blog_edit_manager.html',context)
    else:
        messages.error(request,"Wrong url")
        return redirect('login')


def blogDashboard(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user=request.user
        blogs=BlogManager.objects.filter(user=user.pk)
        context={
            'blogs':blogs,

        }
        return render(request,'blog_dashboard.html',context)
    else:
        messages.error(request,"Wrong url")
        return redirect('login')


def blogcategorycreate(request):
    if request.method=='POST':
        if 'category_submit' in request.POST:
            cag_name=request.POST['cagname']

            if BlogCategory.objects.filter(blog_category=cag_name).exists():
                messages.error(request, 'The Category already exists')
                return redirect('blogcategorycreate')

            if BlogCategory.objects.filter(blog_category=cag_name.upper()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('blogcategorycreate')

            if BlogCategory.objects.filter(blog_category=cag_name.lower()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('blogcategorycreate')

            if BlogCategory.objects.filter(blog_category=cag_name.capitalize()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('blogcategorycreate')


            category_id=BlogCategory.objects.all().count()+1
            cag_obj=BlogCategory(blog_category_id=category_id,blog_category=cag_name)
            cag_obj.save()
            messages.success(request, 'New Category created')

            return redirect('blogcategorycreate')

    return render(request,'blog_create_category.html')
