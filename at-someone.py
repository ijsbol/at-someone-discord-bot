from typing import Final
from os import getenv

from bot import AtSomeoneBot
from dotenv import load_dotenv
from disnake import (
    Intents,
    Activity,
    ActivityType,
)

load_dotenv()

ACTIVITY_NAME: Final[str] = str(getenv("ACTIVITY_STATUS"))
MAXIMUM_SOMEONES_PER_MESSAGE: Final[int] = int(getenv("MAXIMUM_SOMEONES_PER_MESSAGE"))

INTENTS: Final[Intents] = Intents(
    guild_messages=True,
    guilds=True,
    members=True,
)
ACTIVITY: Final[Activity] = Activity(
    name=ACTIVITY_NAME,
    type=ActivityType.listening,
)

bot = AtSomeoneBot(
    intents=INTENTS,
    activity=ACTIVITY,
    MAXIMUM_SOMEONES_PER_MESSAGE=MAXIMUM_SOMEONES_PER_MESSAGE,
)

if __name__ == "__main__":
    bot.run(getenv("DISCORD_BOT_TOKEN"))
