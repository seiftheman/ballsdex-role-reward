from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from role_reward.package import cog as cog_module
from role_reward.package.cog import ProgressionRoleCog

SERVER_ID = 123456789012345678
ROLE_ID = 987654321098765432
MEMBER_ID = 111111111111111111


class FakeRole:
    def __init__(self, role_id: int, position: int = 1, *, managed: bool = False, default: bool = False):
        self.id = role_id
        self.position = position
        self.managed = managed
        self._default = default

    def is_default(self) -> bool:
        return self._default

    def __ge__(self, other: FakeRole) -> bool:
        return self.position >= other.position


class FakeMember:
    def __init__(self, member_id: int, roles: tuple[FakeRole, ...] = ()):
        self.id = member_id
        self.roles = list(roles)
        self.add_roles = AsyncMock()


class FakeBallQuerySet:
    def __init__(self, count: int):
        self.count = count

    def filter(self, **kwargs) -> FakeBallQuerySet:
        return self

    async def acount(self) -> int:
        return self.count


class FakeBallInstanceQuerySet:
    def __init__(self, players: list[int]):
        self.players = players

    def filter(self, *args, **kwargs) -> FakeBallInstanceQuerySet:
        return self

    def values(self, *args) -> FakeBallInstanceQuerySet:
        return self

    def annotate(self, **kwargs) -> FakeBallInstanceQuerySet:
        return self

    def order_by(self, *args) -> FakeBallInstanceQuerySet:
        return self

    def __aiter__(self):
        async def iterate():
            for player_id in self.players:
                yield {"player__discord_id": player_id}

        return iterate()


def make_cog(guild, *, progression: float = 0.5, server_id=SERVER_ID) -> ProgressionRoleCog:
    cog = object.__new__(ProgressionRoleCog)
    cog.bot = SimpleNamespace(
        get_guild=lambda _: guild,
        wait_until_ready=AsyncMock(),
        loop=asyncio.get_running_loop(),
    )
    cog.server_id = server_id
    cog.role_id = ROLE_ID
    cog.progression = progression
    return cog


def make_guild(
    role: FakeRole,
    members: dict[int, FakeMember],
    *,
    manage_roles: bool = True,
    bot_role_position: int = 10,
) -> SimpleNamespace:
    return SimpleNamespace(
        get_role=MagicMock(return_value=role),
        get_member=MagicMock(side_effect=lambda member_id: members.get(member_id)),
        fetch_member=AsyncMock(side_effect=discord.NotFound(MagicMock(), "missing")),
        me=SimpleNamespace(
            guild_permissions=SimpleNamespace(manage_roles=manage_roles),
            top_role=FakeRole(0, bot_role_position),
        ),
    )


def patch_models(monkeypatch, *, total_balls: int = 10, players: list[int] | None = None) -> None:
    monkeypatch.setattr(
        cog_module,
        "Ball",
        SimpleNamespace(objects=SimpleNamespace(filter=lambda **kwargs: FakeBallQuerySet(total_balls))),
    )
    monkeypatch.setattr(
        cog_module,
        "BallInstance",
        SimpleNamespace(
            objects=SimpleNamespace(filter=lambda **kwargs: FakeBallInstanceQuerySet(players or []))
        ),
    )


@pytest.mark.asyncio
async def test_grants_role_to_eligible_member(monkeypatch) -> None:
    role = FakeRole(ROLE_ID)
    member = FakeMember(MEMBER_ID)
    guild = make_guild(role, {MEMBER_ID: member})
    patch_models(monkeypatch, players=[MEMBER_ID])
    cog = make_cog(guild)

    result = await cog._run_progression_check()

    assert result.error is None
    assert result.target_count == 5
    assert result.eligible_players == 1
    assert result.granted == 1
    member.add_roles.assert_awaited_once_with(role, reason="Reached the required progression.")


@pytest.mark.asyncio
async def test_skips_member_who_already_has_role(monkeypatch) -> None:
    role = FakeRole(ROLE_ID)
    member = FakeMember(MEMBER_ID, (role,))
    guild = make_guild(role, {MEMBER_ID: member})
    patch_models(monkeypatch, players=[MEMBER_ID])
    cog = make_cog(guild)

    result = await cog._run_progression_check()

    assert result.already_have_role == 1
    assert result.granted == 0
    member.add_roles.assert_not_awaited()


@pytest.mark.asyncio
async def test_counts_members_missing_from_the_guild(monkeypatch) -> None:
    guild = make_guild(FakeRole(ROLE_ID), {})
    patch_models(monkeypatch, players=[MEMBER_ID])
    cog = make_cog(guild)

    result = await cog._run_progression_check()

    assert result.members_not_found == 1
    assert result.granted == 0


@pytest.mark.asyncio
async def test_unconfigured_settings_return_an_error(monkeypatch) -> None:
    cog = make_cog(None, server_id=None)

    result = await cog._run_progression_check()

    assert "not been configured" in result.error


@pytest.mark.asyncio
async def test_missing_manage_roles_permission_is_reported(monkeypatch) -> None:
    guild = make_guild(FakeRole(ROLE_ID), {}, manage_roles=False)
    patch_models(monkeypatch, players=[MEMBER_ID])
    cog = make_cog(guild)

    result = await cog._run_progression_check()

    assert "Manage Roles" in result.error
    assert result.eligible_players == 0


@pytest.mark.asyncio
async def test_role_above_bot_is_reported(monkeypatch) -> None:
    guild = make_guild(FakeRole(ROLE_ID, position=11), {}, bot_role_position=10)
    patch_models(monkeypatch, players=[MEMBER_ID])
    cog = make_cog(guild)

    result = await cog._run_progression_check()

    assert "below the bot" in result.error


def test_apply_settings_rejects_invalid_progression() -> None:
    cog = object.__new__(ProgressionRoleCog)
    cog.server_id = SERVER_ID
    cog.role_id = ROLE_ID
    cog.progression = 0.5

    cog._apply_settings(SimpleNamespace(server=str(SERVER_ID), role=str(ROLE_ID), progression=0))

    assert (cog.server_id, cog.role_id, cog.progression) == (None, None, None)
