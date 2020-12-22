from django.contrib import admin


from Admin.models import UserDetails,RoleDetail,CareerCategory,SubCategory,CategoryCourse,AdminLicense

# Register your models here.

admin.site.register(UserDetails)
admin.site.register(RoleDetail)
admin.site.register(AdminLicense)


admin.site.register(CareerCategory)
admin.site.register(SubCategory)
admin.site.register(CategoryCourse)
