from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

DISCORD_ID_RE = re.compile(r"^\d{17,21}$")


def validate_progression(value: float) -> None:
    """Ensure the configured progression is a usable fraction (0%, 100%]."""
    if not 0 < value <= 1:
        raise ValidationError("Progression must be greater than 0% and at most 100%.")


class RoleRewardSettings(models.Model):
    server = models.TextField(
        help_text="ID of the Discord server that contains the reward role.",
        validators=(RegexValidator(DISCORD_ID_RE, message="Invalid guild (server) ID."),),
    )
    role = models.TextField(
        help_text="ID of the role that will be given to eligible users.",
        validators=(RegexValidator(DISCORD_ID_RE, message="Invalid role ID."),),
    )
    progression = models.FloatField(
        help_text="Fraction of enabled balls (between 0 and 1) required to receive the reward role.",
        validators=(validate_progression,),
    )

    def clean(self) -> None:
        if RoleRewardSettings.objects.exclude(pk=self.pk).exists():
            raise ValidationError("You can only have one instance of RoleRewardSettings.")

    def __str__(self) -> str:
        return f"Role reward settings (server: {self.server}, role: {self.role})"

    class Meta:
        verbose_name = "Role reward settings"
        verbose_name_plural = "Settings"


async def get_settings() -> RoleRewardSettings | None:
    """Return the single settings row, if one has been configured."""
    return await RoleRewardSettings.objects.order_by("pk").afirst()
