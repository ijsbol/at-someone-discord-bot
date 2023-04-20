from typing import Final, Tuple, List
from random import choice

from disnake import Message, Button
from disnake.ui import View
from disnake.ext.commands import AutoShardedInteractionBot
import cogs

class AtSomeoneBot(AutoShardedInteractionBot):
    def __init__(self, **kwargs) -> None:
        self.MAXIMUM_SOMEONES_PER_MESSAGE: Final[int] = kwargs.pop(
            'MAXIMUM_SOMEONES_PER_MESSAGE', 10
        )

        super().__init__(**kwargs)

        for cog_name in cogs.enabled_cogs:
            self.load_extension(f"cogs.{cog_name}")    

    def generate_mentions_message(
        self,
        guild_member_ids: List[int],
        number_of_mentions: int
    ) -> Tuple[str, bool]:
        maximum_warning = (
            True if number_of_mentions >= self.MAXIMUM_SOMEONES_PER_MESSAGE
            else False
        )

        ids_to_mention: List[int] = []
        number_of_mentions = min(
            number_of_mentions,
            len(guild_member_ids),
            self.MAXIMUM_SOMEONES_PER_MESSAGE,
        )

        for _ in range(number_of_mentions):
            if len(guild_member_ids) != 0:
                id_to_mention = choice(guild_member_ids)
                ids_to_mention.append(id_to_mention)
                guild_member_ids.pop(guild_member_ids.index(id_to_mention))

        mentions = [f"<@{member_id}>" for member_id in ids_to_mention]
        formatted_mentions = (
            '{}, '*(len(mentions)-2) + '{} & '*(len(mentions)>1) + '{}'
        ).format(*mentions)

        return formatted_mentions, maximum_warning

    async def on_message(self, message: Message) -> None:
        if self.user.mentioned_in(message):
            number_of_mentions = sum(
                message.content.count(mention_string) for mention_string in
                    [f"<@!{self.user.id}>", f"<@{self.user.id}>"]
            )
            guild_members = [
                member.id for member in message.guild.members
                if not member.bot
            ]
            mentions_message, maximum_warning = self.generate_mentions_message(
                guild_members,
                number_of_mentions,
            )

            max_mentions_reached_view = None
            if maximum_warning:
                max_mentions_reached_view = View()
                max_mentions_reached_view.add_item(
                    Button(
                        label=f"Maximum of {self.MAXIMUM_SOMEONES_PER_MESSAGE} @someone's per message",
                        disabled=True,
                    )
                )

            await message.reply(
                mention_author=False,
                content=mentions_message,
                view=max_mentions_reached_view,
            )
