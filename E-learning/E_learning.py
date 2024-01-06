import os
import glob
import importlib
import discord
from discord.ext import commands
import asyncio 

class E_learning(commands.Bot):
    async def setup(self):
        # This is the directory that contains all the cogs
        directory = 'C:/Users/saeed/Desktop/Saeed/Year 3/Project/E-learning/E-learning'

        module_files = glob.glob(os.path.join(directory, '*.py'))

        loaded_cogs = []
        unloaded_cogs = []

        # Load each module and register all commands and cogs found
        for module_file in module_files:
            module_name = os.path.splitext(os.path.basename(module_file))[0]
            try:
                module = importlib.import_module(module_name)

                # register all commands and cogs to the bot
                for obj in list(module.__dict__.values()):
                    if isinstance(obj, commands.Command):
                        self.add_command(obj)
                    elif isinstance(obj, type) and issubclass(obj, commands.Cog):
                        await self.add_cog(obj(self))

                loaded_cogs.append(module_name)
            except Exception as e:
                unloaded_cogs.append(module_name)
                print(f"Failed to load module {module_name}: {e}")

        # Print the list of loaded and unloaded cogs, this is done so it helps figure out which cogs don't work
        print("Cogs loaded succesfully:")
        print("\n".join(loaded_cogs))
        print("Cogs failed to load:")
        print("\n".join(unloaded_cogs))

    async def on_ready(self):
        print(f'Bot is online')
        await self.setup()


async def main():
    #set the Bot Token
    Bot_Token = 'MTA3OTg1NDUwNjQ2NjEwMzM2Nw.Gzp4gX.XbcAz3aqQUlR7OVbXjwGfjkmaGy-Itfn17wDvc'

    bot = E_learning(command_prefix='?', intents=discord.Intents.all())
    await bot.start(Bot_Token)


if __name__ == '__main__':
    asyncio.run(main())
