from django.contrib import admin

from sport.models import Activity, Sport, SportUser

# Register your models here.
admin.site.register(Sport)
admin.site.register(Activity)
admin.site.register(SportUser)