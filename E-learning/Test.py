import discord
from discord.ext import commands 

class Test(commands.Cog, name='test'):
   
    def __init__(self, bot):
        self.bot = bot
    #Checks if the website is working
    @commands.command(description = "This test if the bot is online")
    async def test(self, ctx):
        await ctx.send("Bot is online")
    #Sends the link of the website
    @commands.command(description = "This will post the website of the bot")
    async def website(self, ctx):
        await ctx.send("Print the website out")


def setup(bot):    
    bot.add_cog(Test(bot))
