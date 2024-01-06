import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}


    async def has_teacher_role(self, ctx):
        teacher_role = discord.utils.get(ctx.guild.roles, name="Teacher")
        return teacher_role in ctx.author.roles


    #This will mute the user, which means it will disable the send_messages perms for him in all channels in the server
    @commands.command(description = "This will mute a user from typing in chat")
    async def mute(self, ctx, member: discord.Member):
        teacher_role = discord.utils.get(ctx.guild.roles, name="Teacher")
        if await self.has_teacher_role(ctx):
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not role:
                role = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, send_messages=False, speak=False)
            await member.add_roles(role)
            await ctx.send(f"{ctx.author.mention}, {member.mention} This user has been muted.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have permission to mute a user. Please assign the `Teacher` role to yourself in order to succesfully use this command. You can do this by typing  'verify_teacher @yourself' ")

    #This will unmute the user, which means it will enable the send_messages perms for him in all channels in the server
    @commands.command(description = "This will unmute a member")
    async def unmute(self, ctx, member: discord.Member):
        teacher_role = discord.utils.get(ctx.guild.roles, name="Teacher")
        if await self.has_teacher_role(ctx):
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"{ctx.author.mention}, {member.mention} has been unmuted.")
            else:
                await ctx.send(f"{ctx.author.mention}, {member.mention} is not currently muted.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have permission to unmute a user. Please assign the `Teacher` role to yourself in order to succesfully use this command. You can do this by typing  'verify_teacher @yourself'.")

    #This will create a message as a warning for a specific user and add it to a dictionary which can be viewed by using listwarnings command
    @commands.command(description = "This will register a warning for a user")
    async def warn(self, ctx, member: discord.Member, *, warning: str = None):
        if await self.has_teacher_role(ctx):
            if warning is None:
                await ctx.send(f"{ctx.author.mention} Please provide a reason for the warning. For example: `?testwarn @user [warning_message]`")
                return

            if str(member.id) not in self.warnings:
                self.warnings[str(member.id)] = [] 
            self.warnings[str(member.id)].append(warning)
            await ctx.send(f"{ctx.author.mention}, {member.mention} has been warned: {warning}")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have permission to add a warning. Please assign the `Teacher` role to yourself in order to succesfully use this command. You can do this by typing  'verify_teacher @yourself'")
    #This will list all the user's warnings 
    @commands.command(description = "This will list the amount of warnings a user got")
    async def listwarnings(self, ctx, member: discord.Member):
        if await self.has_teacher_role(ctx):
            warnings = self.warnings.get(str(member.id), [])
            if warnings:
                warning_list = "\n".join(f"{i+1}. {warning}" for i, warning in enumerate(warnings))
                await ctx.send(f"Warnings for {member.mention}:\n{warning_list}")
            else:
                await ctx.send(f"{member.mention} has no warnings.")
        else:
            await ctx.send("{ctx.author.mention} You do not have permission to list the warnings of a user. Please assign the `Teacher` role to yourself in order to succesfully use this command. You can do this by typing  'verify_teacher @yourself'")
     #This will kick a user out of a server
    @commands.command(description = "This will kick a member out of the server")
    async def kick(self, ctx, member: discord.Member):
        teacher_role = discord.utils.get(ctx.guild.roles, name="Teacher")
        if await self.has_teacher_role(ctx):
            await member.kick()
            await ctx.send(f"{ctx.author.mention}, {member.mention} has been kicked from the server.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have permission to kick a user.Please assign the `Teacher` role to yourself in order to succesfully use this command. You can do this by typing  'verify_teacher @yourself'")

     #This will ban a user out of a server
    @commands.command(description = "This will ban a member out of the server")
    async def ban(self, ctx, member: discord.Member):
        teacher_role = discord.utils.get(ctx.guild.roles, name="Teacher")
        if await self.has_teacher_role(ctx):
            await member.ban()
            await ctx.send(f"{ctx.author.mention}, {member.mention} This user has been banned from the server.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have permission to ban a user. Please assign the `Teacher` role to yourself in order to succesfully use this command. You can do this by typing  'verify_teacher @yourself'")




def setup(bot):
    bot.add_cog(Moderation(bot))
