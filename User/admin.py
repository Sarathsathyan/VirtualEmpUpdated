from django.contrib import admin


from .models import UserContact,UserEducation,UserWorkExperience,UserSkill,CareerChoice

# Register your models here.


admin.site.register(UserContact)
admin.site.register(UserEducation)
admin.site.register(UserWorkExperience)
admin.site.register(UserSkill)
admin.site.register(CareerChoice)
