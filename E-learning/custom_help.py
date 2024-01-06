import discord
from discord.ext import commands

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = CustomHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

class CustomHelpCommand(commands.HelpCommand):
    # This will send a list of all commands in the bot
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=discord.Color.blue())
        for cog, commands in mapping.items():
            if cog:
                cog_name = cog.qualified_name
                command_names = [command.name for command in commands]
                if command_names:
                    command_list = ", ".join(command_names)
                    embed.add_field(name=cog_name, value=command_list, inline=False)
        await self.get_destination().send(embed=embed)

    # This will send a description of the command
    async def send_command_help(self, command):
        embed = discord.Embed(title=command.name, color=discord.Color.blue())
        embed.add_field(name="Description", value=command.description, inline=False)
        embed.add_field(name="Usage", value=f"{self.context.prefix}{command.name} {command.signature}", inline=False)
        await self.get_destination().send(embed=embed)

def setup(bot):
    bot.add_cog(CustomHelp(bot))
