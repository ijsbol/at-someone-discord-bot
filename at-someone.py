from discord import (
    Intents,
    Activity,
    ActivityType,
    Message
)
from discord.ui import (
    View,
    Button
)
from discord.ext import commands
from typing import List, Final
import random

intents: Intents = Intents.none()
intents.guild_messages: bool = True
intents.message_content: bool = False
intents.guilds: bool = True
intents.members: bool = True

MAXIMUM_SOMEONES_PER_MESSAGE: Final[int] = 10

bot: commands.AutoShardedBot = commands.AutoShardedBot(
    intents=intents, 
    activity=Activity(
        name="you type @someone", 
        type=ActivityType.listening
    )
)

def generate_mentions_message(guild_member_ids: List[int], number_of_mentions: int) -> (str, bool):
    maximum_warning: bool = False
    if number_of_mentions > MAXIMUM_SOMEONES_PER_MESSAGE and len(guild_member_ids) > MAXIMUM_SOMEONES_PER_MESSAGE:
        number_of_mentions: bool = MAXIMUM_SOMEONES_PER_MESSAGE
        maximum_warning: bool = True
    ids_to_mention: List[int] = []
    for i in range(number_of_mentions):
        if len(guild_member_ids) != 0:
            id_to_mention: int = random.choice(guild_member_ids)
            ids_to_mention.append(id_to_mention)
            guild_member_ids.pop(guild_member_ids.index(id_to_mention))
    del guild_member_ids, i
    mentions = [f"<@{member_id}>" for member_id in ids_to_mention]
    return ('{}, '*(len(mentions)-2) + '{} & '*(len(mentions)>1) + '{}').format(*mentions), maximum_warning

@bot.listen('on_message')
async def on_message_handler(message: Message) -> None:
    if "@someone" in message.content or bot.user.mentioned_in(message):
        number_of_mentions: int = 0
        number_of_mentions += message.content.count("@someone")
        number_of_mentions += message.content.count(f"<@!{bot.user.id}>")
        number_of_mentions += message.content.count(f"<@{bot.user.id}>")
        mentions_message, maximum_warning = generate_mentions_message([member.id for member in message.guild.members if not member.bot], number_of_mentions)

        del number_of_mentions

        MAX_MENTIONS_REACHED_VIEW: View = View()
        MAX_MENTIONS_REACHED_VIEW.add_item(Button(label=f"Maximum of {MAXIMUM_SOMEONES_PER_MESSAGE} @someone's per message", disabled=True))

        await message.reply(
            mention_author=False, 
            content=mentions_message, 
            view=MAX_MENTIONS_REACHED_VIEW if maximum_warning else None,
        )

bot.run("BOT_TOKEN")
