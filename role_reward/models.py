from __future__ import annotations

import re

from django.core.validators import RegexValidator
from django.db import models
from django.forms import ValidationError

DISCORD_ID_RE = re.compile(r"^\d{17,21}$")
COLON_IDS_RE = re.compile(r"^(\d{17,21}(;\d{17,21})*)?$")


class RoleRewardSettings(models.Model):
    server = models.TextField(
        help_text="Server ID that has the reward role.",
        validators=(RegexValidator(DISCORD_ID_RE, message="Invalid guild (server) ID."),),
    )
    role = models.TextField(
        help_text="Role that will be given to users.",
        validators=(RegexValidator(DISCORD_ID_RE, message="Invalid forum channel ID."),),
    )
    progression = models.FloatField(
        help_text="Progression of the bot required for users to be given the reward role."
    )
    def clean(self) -> None:
        if RoleRewardSettings.objects.exclude(pk=self.pk).exists():
            raise ValidationError("You can only have one instance of RoleRewardSettings.")

    def __str__(self) -> str:
        return "Role reward package settings"

    class Meta:
        verbose_name_plural = "Settings"

async def get_settings():
    return await RoleRewardSettings.objects.afirst() or await RoleRewardSettings.objects.acreate()
