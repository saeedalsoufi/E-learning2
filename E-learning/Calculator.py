import discord
from discord.ext import commands


class Calculator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    #This is the add function
    @commands.command(description = "This function is used to add up numbers")
    async def add(self, ctx, *arr):
        result = 0 
        for i in arr:
            try:

                result += float(i)
            except ValueError:
                await ctx.send (f"This function only works on whole numbers")
                return

        await ctx.send(f"Result: {result}")
    #This is the minus function
    @commands.command(description = "This function is used to take away numbers from eachother")
    async def minus(self, ctx, *arr):
        try:
            result = float(arr[0])
            for i in arr[1:]:
                result -= float(i)
        except ValueError:
                await ctx.send (f"This function only works on whole numbers")
                return
        await ctx.send(f"Result: {result}")
    #This is the times function
    @commands.command(description = "This function only works on multiplying numbers")
    async def times(self, ctx, *arr):
        result = 1
        for i in arr:
            try:
                result *= float(i)
            except ValueError:
                await ctx.send (f"This function only works on whole numbers")
                return
        await ctx.send(f"Result: {result}")
    #This is the divide function
    @commands.command(description = "This function divide numbers from eachother")
    async def divide(self, ctx, *arr):
        try:
            result = float(arr[0])
            for i in arr[1:]:
                result /= float(i)
        except ValueError:
                await ctx.send (f"This function only works on whole numbers")
                return
        await ctx.send(f"Result: {result}")
    

#Add the commands of this cog to the bot
def setup(bot):
    print('Loading Test cog...')    
    bot.add_cog(Calculator(bot))




