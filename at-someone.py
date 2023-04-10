from discord import (
    Intents,
    Activity,
    ActivityType,
    Message,
)
from discord.ui import View, Button
from discord.ext.commands import AutoShardedBot
from typing import List, Final, Tuple
from random import choice

INTENTS: Final[Intents] = Intents(
    guild_messages=True,
    message_content=True,
    guilds=True,
    members=True,
)
ACTIVITY: Final[Activity] = Activity(
    name="you type @someone",
    type=ActivityType.listening,
)
MAXIMUM_SOMEONES_PER_MESSAGE: Final[int] = 10

bot = AutoShardedBot(
    intents=INTENTS,
    activity=ACTIVITY,
)

def generate_mentions_message(guild_member_ids: List[int], number_of_mentions: int) -> Tuple[str, bool]:
    maximum_warning = False
    if (
        number_of_mentions > MAXIMUM_SOMEONES_PER_MESSAGE
        and len(guild_member_ids) > MAXIMUM_SOMEONES_PER_MESSAGE
    ):
        number_of_mentions = MAXIMUM_SOMEONES_PER_MESSAGE
        maximum_warning = True

    ids_to_mention: List[int] = []

    for mention_num in range(number_of_mentions):
        if len(guild_member_ids) != 0:
            id_to_mention = choice(guild_member_ids)
            ids_to_mention.append(id_to_mention)
            guild_member_ids.pop(guild_member_ids.index(id_to_mention))

    del guild_member_ids, mention_num

    mentions = [f"<@{member_id}>" for member_id in ids_to_mention]
    formatted_mentions = ('{}, '*(len(mentions)-2) + '{} & '*(len(mentions)>1) + '{}').format(*mentions)

    return formatted_mentions, maximum_warning

@bot.listen('on_message')
async def on_message(message: Message) -> None:
    if "@someone" in message.content or bot.user.mentioned_in(message):
        number_of_mentions = sum(
            message.content.count(mention_string) for mention_string in
                ["@someone", f"<@!{bot.user.id}>", f"<@{bot.user.id}>"]
        )
        guild_members = [member.id for member in message.guild.members if not member.bot]
        mentions_message, maximum_warning = generate_mentions_message(guild_members, number_of_mentions)

        del number_of_mentions

        max_mentions_reached_view = None
        if maximum_warning:
            max_mentions_reached_view = View()
            max_mentions_reached_view.add_item(Button(label=f"Maximum of {MAXIMUM_SOMEONES_PER_MESSAGE} @someone's per message", disabled=True))

        await message.reply(
            mention_author=False,
            content=mentions_message,
            view=max_mentions_reached_view,
        )

bot.run("BOT_TOKEN")
