from django.contrib import admin
from django.db import models
from django.forms import widgets

from .models import RoleRewardSettings


@admin.register(RoleRewardSettings)
class RoleRewardSettingsAdmin(admin.ModelAdmin):
    save_on_top = True
    formfield_overrides = {models.TextField: {"widget": widgets.TextInput}}
    fieldsets = [
        (None, {"fields": ("server", "role", "progression")}),
    ]
