from __future__ import annotations

from asgiref.sync import async_to_sync
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase

from role_reward.models import RoleRewardSettings, get_settings

SERVER_ID = "123456789012345678"
ROLE_ID = "987654321098765432"


class FieldValidationTests(SimpleTestCase):
    def setUp(self) -> None:
        self.server_field = RoleRewardSettings._meta.get_field("server")
        self.role_field = RoleRewardSettings._meta.get_field("role")
        self.progression_field = RoleRewardSettings._meta.get_field("progression")

    def test_accepts_valid_values(self) -> None:
        self.assertEqual(self.server_field.clean(SERVER_ID, None), SERVER_ID)
        self.assertEqual(self.role_field.clean(ROLE_ID, None), ROLE_ID)
        self.assertEqual(self.progression_field.clean(0.5, None), 0.5)
        self.assertEqual(self.progression_field.clean(1.0, None), 1.0)

    def test_rejects_invalid_ids(self) -> None:
        with self.assertRaisesMessage(ValidationError, "Invalid guild (server) ID"):
            self.server_field.clean("not-an-id", None)
        with self.assertRaisesMessage(ValidationError, "Invalid role ID"):
            self.role_field.clean("123", None)

    def test_rejects_out_of_range_progression(self) -> None:
        for value in (0, -0.1, 1.1):
            with self.subTest(value=value):
                with self.assertRaisesMessage(ValidationError, "greater than 0%"):
                    self.progression_field.clean(value, None)


class SettingsTests(TestCase):
    def test_only_one_settings_row_is_allowed(self) -> None:
        RoleRewardSettings.objects.create(server=SERVER_ID, role=ROLE_ID, progression=0.1)
        duplicate = RoleRewardSettings(server=SERVER_ID, role=ROLE_ID, progression=0.2)

        with self.assertRaises(ValidationError) as error:
            duplicate.full_clean()
        self.assertIn("only have one instance", str(error.exception))

    def test_get_settings_returns_first_row(self) -> None:
        first = RoleRewardSettings.objects.create(server=SERVER_ID, role=ROLE_ID, progression=0.1)
        RoleRewardSettings.objects.create(server=SERVER_ID, role=ROLE_ID, progression=0.2)

        self.assertEqual(async_to_sync(get_settings)().pk, first.pk)

    def test_get_settings_returns_none_when_unconfigured(self) -> None:
        self.assertIsNone(async_to_sync(get_settings)())
