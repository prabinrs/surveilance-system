from django.contrib import admin

from .models import (
    CronSetting
)


@admin.register(CronSetting)
class CronSettingAdmin(admin.ModelAdmin):
    pass

