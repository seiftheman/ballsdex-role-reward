"""Shared test setup: configure Django and stub the BallsDex-only dependencies."""

from __future__ import annotations

import sys
import types

import django
import pytest
from django.conf import settings
from django.test.utils import setup_databases, teardown_databases

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "role_reward",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        SECRET_KEY="role-reward-tests",
        USE_TZ=True,
    )
    django.setup()

# ``bd_models`` is only available inside a BallsDex installation. The cog tests
# replace these classes with fakes, but the import must still resolve here.
if "bd_models.models" not in sys.modules:
    bd_models = sys.modules.setdefault("bd_models", types.ModuleType("bd_models"))
    bd_models.__path__ = []  # type: ignore[attr-defined]

    bd_models_models = types.ModuleType("bd_models.models")

    class Ball:  # pragma: no cover - replaced in tests
        pass

    class BallInstance:  # pragma: no cover - replaced in tests
        pass

    bd_models_models.Ball = Ball
    bd_models_models.BallInstance = BallInstance
    sys.modules["bd_models.models"] = bd_models_models


@pytest.fixture(scope="session", autouse=True)
def django_test_database():
    """Create the test database since pytest-django is not a dependency."""
    old_config = setup_databases(verbosity=0, interactive=False)
    yield
    teardown_databases(old_config, verbosity=0)
