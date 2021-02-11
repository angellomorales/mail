from django.contrib import admin

from .models import Email,User 

# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    list_display=("id","sender","get_recipients","subject","timestamp","read","archived")

admin.site.register(User)
admin.site.register(Email,EmailAdmin)