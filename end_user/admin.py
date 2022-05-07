from django.contrib import admin
from . import models


@admin.register(models.EndUser)
class EndUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Preference)
class PreferenceAdmin(admin.ModelAdmin):
    pass
