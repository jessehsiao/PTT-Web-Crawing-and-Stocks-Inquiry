from django.contrib import admin
from jesseapp.models import user
# Register your models here.
class userAdmin(admin.ModelAdmin):
    list_disply = ('userID',)
    
admin.site.register(user, userAdmin)