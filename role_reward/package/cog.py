import logging
import asyncio
import discord
from discord import app_commands
from discord.ext import commands, tasks
from django.db.models import Count
from role_reward.models import get_settings
from bd_models.models import Ball, BallInstance

log = logging.getLogger("ballsdex.packages.role_reward")

class ProgressionRoleCog(commands.Cog):
    """Role reward commands."""

    def __init__(self, bot):
        self.bot = bot
        settings = get_settings()
        server_id = settings.server()
        role_id = settings.role()
        progression = settings.progression()
        self.check_progression.start()

    def cog_unload(self):
        self.check_progression.cancel()

    async def _check_and_reward_user(self, member: discord.Member, guild: discord.Guild, role: discord.Role, total_balls: int) -> bool:
        """Returns True if the role was given."""
        if role in member.roles:
            return False

        owned_countryballs_count = await BallInstance.objects.filter(
            player__discord_id=member.id, ball__enabled=True
        ).values("ball_id").distinct().acount()

        progression = owned_countryballs_count / total_balls if total_balls > 0 else 0
        if progression >= self.progression:
            try:
                await member.add_roles(role, reason="Reached the required progression.")
                log.info(f"Granted progression reward role to {member.id}.")
                return True
            except discord.Forbidden:
                log.error("Failed to add role due to missing permissions.")
            except discord.HTTPException as e:
                log.error(f"Failed to add role due to HTTP error: {e}")
        return False

    @tasks.loop(minutes=5)
    async def check_progression(self):
        await self.bot.wait_until_ready()
        
        guild = self.bot.get_guild(self.server_id)
        if not guild:
            return
            
        role = guild.get_role(self.role_id)
        if not role:
            return

        total_balls = await Ball.objects.filter(enabled=True).acount()
        if total_balls == 0:
            return

        import math
        target_count = math.ceil(total_balls * 0.005)

        players_with_enough_balls = []
        async for player_dict in BallInstance.objects.filter(ball__enabled=True).values('player__discord_id').annotate(
            distinct_balls=Count('ball_id', distinct=True)
        ).order_by().filter(distinct_balls__gte=target_count):
            players_with_enough_balls.append(player_dict['player__discord_id'])

        for discord_id in players_with_enough_balls:
            member = guild.get_member(discord_id)
            if not member:
                try:
                    member = await guild.fetch_member(discord_id)
                except discord.NotFound:
                    member = None
            
            if member and role not in member.roles:
                try:
                    await member.add_roles(role, reason="Reached the required progression.")
                    log.info(f"Granted progression reward role to {member.id}.")
                except discord.HTTPException:
                    pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def hello(self, ctx: commands.Context):
        """Manually trigger the progression role check for the server."""
        if ctx.guild and ctx.guild.id != self.server_id:
            return
            
        guild = self.bot.get_guild(self.server_id)
        role = guild.get_role(self.role_id)
        if not role:
            await ctx.send("The reward role is not configured correctly on the server.")
            return

        total_balls = await Ball.objects.filter(enabled=True).acount()

        import math
        target_count = math.ceil(total_balls * 0.005)

        players_with_enough_balls = []
        async for player_dict in BallInstance.objects.filter(ball__enabled=True).values('player__discord_id').annotate(
            distinct_balls=Count('ball_id', distinct=True)
        ).order_by().filter(distinct_balls__gte=target_count):
            players_with_enough_balls.append(player_dict['player__discord_id'])

        given = 0
        already_have = 0
        not_found = 0
        
        status_msg = await ctx.send(f"Found {len(players_with_enough_balls)} players in the database with >= {target_count}/{total_balls} balls (0.5%). Checking members...")

        for discord_id in players_with_enough_balls:
            member = guild.get_member(discord_id)
            if not member:
                try:
                    member = await guild.fetch_member(discord_id)
                except discord.NotFound:
                    member = None
                    
            if not member:
                not_found += 1
                continue

            if role in member.roles:
                already_have += 1
            else:
                try:
                    await member.add_roles(role, reason="Reached the required progression.")
                    log.info(f"Granted progression reward role to {member.id}.")
                    given += 1
                except discord.HTTPException:
                    pass

        await status_msg.edit(content=f"Role check complete (Target: {target_count}/{total_balls} balls).\n"
                                      f"Total eligible players in DB: {len(players_with_enough_balls)}\n"
                                      f"Already have the role: {already_have}\n"
                                      f"Not found in server: {not_found}\n"
                                      f"Newly assigned the role to: {given} members.")
