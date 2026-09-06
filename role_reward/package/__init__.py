from .cog import ProgressionRoleCog
from role_reward.models import get_settings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

async def setup(bot: "BallsDexBot") -> None:
    settings = await get_settings()
    await bot.add_cog(
        ProgressionRoleCog(
            bot,
            server_id=int(settings.server),
            role_id=int(settings.role),
            progression=settings.progression,
        )
    )
