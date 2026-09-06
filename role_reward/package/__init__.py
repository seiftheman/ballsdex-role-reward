import logging
from .cog import ProgressionRoleCog
from role_reward.models import get_settings
from typing import TYPE_CHECKING

log = logging.getLogger("ballsdex.packages.role_reward")

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

async def setup(bot: "BallsDexBot") -> None:
    settings = await get_settings()
    if settings is None:
        log.warning("Role reward settings have not been configured; cog was not loaded.")
        return

    await bot.add_cog(
        ProgressionRoleCog(
            bot,
            server_id=int(settings.server),
            role_id=int(settings.role),
            progression=settings.progression,
        )
    )
