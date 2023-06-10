from django.contrib import admin
from .models import CvForm,Profile


class CvFormAdmin(admin.ModelAdmin):
    list_display = ('logo_url', 'position', 'employer', 'salary', 'salary_taxes', 'how_old_ad', 'ad_link', 'work_area')


admin.site.register(CvForm)
admin.site.register(Profile)