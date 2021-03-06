from django.contrib import admin
from Ratecompany.models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location','salary', 'wellfare', 'atmosphere','emailtag')
    prepopulated_fields = {'slug':('name',)}

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comments', 'date')

admin.site.register(UserProfile)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Comments,CommentsAdmin)

