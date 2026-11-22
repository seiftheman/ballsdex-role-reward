import logging
from dataclasses import dataclass

import discord
from discord.ext import commands, tasks
from django.db.models import Count
from django.db.models.signals import post_delete, post_save

from bd_models.models import Ball, BallInstance
from role_reward.models import RoleRewardSettings, get_settings
from role_reward.progression import required_distinct_balls

log = logging.getLogger("ballsdex.packages.role_reward")


@dataclass(slots=True)
class ProgressionCheckResult:
    total_balls: int = 0
    target_count: int = 0
    eligible_players: int = 0
    granted: int = 0
    already_have_role: int = 0
    members_not_found: int = 0
    assignment_failures: int = 0
    error: str | None = None


class ProgressionRoleCog(commands.Cog):
    """Award a role to players who meet the configured collection progression."""

    def __init__(self, bot):
        self.bot = bot
        self.server_id: int | None = None
        self.role_id: int | None = None
        self.progression: float | None = None
        post_save.connect(
            self._settings_saved,
            sender=RoleRewardSettings,
            dispatch_uid="role_reward.progression_role_settings_saved",
            weak=False,
        )
        post_delete.connect(
            self._settings_deleted,
            sender=RoleRewardSettings,
            dispatch_uid="role_reward.progression_role_settings_deleted",
            weak=False,
        )
        self.check_progression.start()

    def cog_unload(self):
        self.check_progression.cancel()
        post_save.disconnect(
            sender=RoleRewardSettings,
            dispatch_uid="role_reward.progression_role_settings_saved",
        )
        post_delete.disconnect(
            sender=RoleRewardSettings,
            dispatch_uid="role_reward.progression_role_settings_deleted",
        )

    def _settings_saved(self, sender, instance: RoleRewardSettings, **kwargs):
        self.bot.loop.call_soon_threadsafe(self._apply_settings, instance)

    def _settings_deleted(self, sender, **kwargs):
        self.bot.loop.call_soon_threadsafe(self._clear_settings)

    def _apply_settings(self, settings: RoleRewardSettings):
        try:
            server_id = int(settings.server)
            role_id = int(settings.role)
            progression = float(settings.progression)
        except (TypeError, ValueError):
            self._clear_settings()
            log.error("Role reward settings contain invalid values.")
            return

        if not 0 < progression <= 1:
            self._clear_settings()
            log.error(
                "Role reward progression must be greater than 0%% and at most 100%% (got %.2f%%).",
                progression * 100,
            )
            return

        self.server_id = server_id
        self.role_id = role_id
        self.progression = progression

        log.info(
            "Loaded role reward settings for guild %s: role %s at %.2f%% progression.",
            self.server_id,
            self.role_id,
            self.progression * 100,
        )

    def _clear_settings(self):
        self.server_id = None
        self.role_id = None
        self.progression = None

    async def reload_settings(self) -> bool:
        settings = await get_settings()
        if settings is None:
            self._clear_settings()
            return False

        self._apply_settings(settings)
        return self.server_id is not None and self.role_id is not None and self.progression is not None

    async def _run_progression_check(self) -> ProgressionCheckResult:
        if self.server_id is None or self.role_id is None or self.progression is None:
            return ProgressionCheckResult(error="Role reward settings have not been configured.")

        progression = self.progression
        guild = self.bot.get_guild(self.server_id)
        if guild is None:
            return ProgressionCheckResult(error="The configured server is unavailable to the bot.")

        role = guild.get_role(self.role_id)
        if role is None:
            return ProgressionCheckResult(error="The configured reward role was not found in the server.")

        bot_member = guild.me
        if bot_member is None or not bot_member.guild_permissions.manage_roles:
            return ProgressionCheckResult(
                error="The bot needs the 'Manage Roles' permission in the configured server."
            )
        if role.is_default() or role.managed or role >= bot_member.top_role:
            return ProgressionCheckResult(
                error="The reward role is managed by Discord or is not below the bot's highest role."
            )

        total_balls = await Ball.objects.filter(enabled=True).acount()
        if total_balls == 0:
            return ProgressionCheckResult(error="There are no enabled balls to calculate progression from.")

        try:
            target_count = required_distinct_balls(total_balls, progression)
        except ValueError as exc:
            return ProgressionCheckResult(error=str(exc))

        eligible_player_ids = [
            player["player__discord_id"]
            async for player in BallInstance.objects.filter(ball__enabled=True)
            .values("player__discord_id")
            .annotate(distinct_balls=Count("ball_id", distinct=True))
            .order_by()
            .filter(distinct_balls__gte=target_count)
        ]
        result = ProgressionCheckResult(
            total_balls=total_balls,
            target_count=target_count,
            eligible_players=len(eligible_player_ids),
        )

        for discord_id in eligible_player_ids:
            member = guild.get_member(discord_id)
            if member is None:
                try:
                    member = await guild.fetch_member(discord_id)
                except discord.NotFound:
                    result.members_not_found += 1
                    continue
                except discord.HTTPException:
                    result.assignment_failures += 1
                    log.exception("Failed to fetch member %s for a role reward check.", discord_id)
                    continue

            if role in member.roles:
                result.already_have_role += 1
                continue

            try:
                await member.add_roles(role, reason="Reached the required progression.")
            except discord.Forbidden:
                result.assignment_failures += 1
                log.error("Cannot grant the progression reward role to %s due to missing permissions.", member.id)
            except discord.HTTPException:
                result.assignment_failures += 1
                log.exception("Failed to grant the progression reward role to %s.", member.id)
            else:
                result.granted += 1
                log.info("Granted progression reward role to %s.", member.id)

        log.info(
            "Progression check: %s enabled balls, %.2f%% required, target %s balls, "
            "%s eligible, %s granted, %s already rewarded, %s members missing, %s failures.",
            result.total_balls,
            progression * 100,
            result.target_count,
            result.eligible_players,
            result.granted,
            result.already_have_role,
            result.members_not_found,
            result.assignment_failures,
        )
        return result

    @tasks.loop(minutes=5)
    async def check_progression(self):
        await self.bot.wait_until_ready()
        if not await self.reload_settings():
            log.warning("Progression check skipped: Role reward settings have not been configured.")
            return

        result = await self._run_progression_check()
        if result.error:
            log.warning("Progression check skipped: %s", result.error)

    @commands.command(name="rolereward", aliases=("hello",))
    @commands.is_owner()
    async def role_reward_check(self, ctx: commands.Context):
        """Manually run the progression role check for the configured server."""
        await self.bot.wait_until_ready()
        if not await self.reload_settings():
            await ctx.send("Role reward settings have not been configured yet.")
            return

        if ctx.guild is None or ctx.guild.id != self.server_id:
            await ctx.send("This command can only be used in the configured server.")
            return

        result = await self._run_progression_check()
        if result.error:
            await ctx.send(result.error)
            return

        await ctx.send(
            "Progression role check complete.\n"
            f"Enabled balls: {result.total_balls}\n"
            f"Required progression: {self.progression:.2%}\n"
            f"Target: {result.target_count}/{result.total_balls} distinct balls\n"
            f"Eligible players: {result.eligible_players}\n"
            f"Already rewarded: {result.already_have_role}\n"
            f"Members not found: {result.members_not_found}\n"
            f"Newly assigned: {result.granted}\n"
            f"Failures: {result.assignment_failures}"
        )
