from .cog import ProgressionRoleCog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

async def setup(bot: "BallsDexBot") -> None:
    await bot.add_cog(ProgressionRoleCog(bot))
