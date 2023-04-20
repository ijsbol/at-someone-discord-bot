from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Cog, Range, Range, slash_command
from bot import AtSomeoneBot

class SlashCommands(Cog):
    """For slash commands."""

    def __init__(self, bot: AtSomeoneBot) -> None:
        self.bot = bot

    @slash_command(
        name="atsomeone",
        description="Mention random user(s) on Discord.",
    )
    async def random_mention(
        self,
        interaction: ApplicationCommandInteraction,
        number: Range[1, 10],
    ) -> None:
        guild_members = [
            member.id for member in interaction.guild.members
            if not member.bot
        ]
        mentions_message, _ = self.bot.generate_mentions_message(
            guild_members,
            number,
        )

        return await interaction.response.send_message(
            content=mentions_message,
        )

def setup(bot: AtSomeoneBot) -> None:
    bot.add_cog(SlashCommands(bot))