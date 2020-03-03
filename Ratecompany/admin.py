from django.contrib import admin
from Ratecompany.models import Category,Company,Comments

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','rates','location')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comments','date')


admin.site.register(Category,CategoryAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Comments,CommentsAdmin)

