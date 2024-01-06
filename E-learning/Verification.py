from discord.ext import commands
import discord
import traceback

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #This function creates the command that activites the verification system.
    @commands.command(description = "This will create a channel which will make it so when new members join the server they can only see it till they get verified.")
    @commands.has_permissions(administrator=True)
    async def activeverify(self, ctx):
        try:
            await ctx.send(f"{ctx.author.mention}, Please type 'yes' to activate the verification system or 'no' to cancel.")
            response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            #Creates the verification category with type-here channel.
            if response.content.lower() == "yes":
                verification_category = await ctx.guild.create_category("Verification")
                await verification_category.create_text_channel("type-here")

                # Deny read and send permissions for the @everyone role in the category (This is used so members who gets verified don't see this category anymore)
                await verification_category.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)

                await ctx.send(f"{ctx.author.mention}, the verification system is now activated.")

            elif response.content.lower() == "no":
                await ctx.send(f"{ctx.author.mention}, the verification system activation process has been canceled.")
            else:
                await ctx.send(f"{ctx.author.mention}, Please type 'yes' or 'no'.")
        except Exception as error:
            await ctx.send(f"{ctx.author.mention} An error occurred: {error}, please try report it and try again later")
            traceback.print_exc()


    #This function will cahnge perms of every channel in the server making it so new users can't view the channels. 
    @commands.Cog.listener()
    async def on_member_join(self, member):
        #Checks if the verification category is created which means the verification process is activated.
        try:
            verification_category = discord.utils.get(member.guild.categories, name="Verification")

            for channel in member.guild.channels:
                if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
                    if channel.category_id == verification_category.id:
                        await channel.set_permissions(member, read_messages=True, send_messages=True)
                    else:
                        await channel.set_permissions(member, read_messages=False, send_messages=False)

        except Exception as error:
            await ctx.send(f"{ctx.author.mention} An error occurred: {error}, please try report it and try again later")
            traceback.print_exc()



    #This function will reset the member's permissions in all channels. This function is written 
    # to allow new users who can't see any channels to be able to view them now by
    #calling the functon in verify_student and verify_teacher
    async def verify_member(self, member):
        verification_category = discord.utils.get(member.guild.categories, name="Verification")

        if verification_category is not None:
            for channel in member.guild.channels:
                await channel.set_permissions(member, overwrite=None)

    #This function will create a student role and give it to a member, then it will verify them and allow them to see the whole server.
    @commands.command(description = "This will verify members as students")
    @commands.has_permissions(administrator=True)
    async def verify_student(self, ctx, member: discord.Member):
        try:
            student_role = discord.utils.get(ctx.guild.roles, name="Student")

            if not student_role:
                student_role = await ctx.guild.create_role(name="Student")

            await member.add_roles(student_role)
            await self.verify_member(member)
            await ctx.send(f"{ctx.author.mention}, {member.mention} has been verified as a student.")
        except Exception as error:
            await ctx.send(f"{ctx.author.mention} An error occurred: {error}, please try report it and try again later")
            traceback.print_exc()


    #This function will create a student role and give it to a member, then it will verify them and allow them to see the whole server.
    @commands.command(description = "This will verify members as a teacher")
    @commands.has_permissions(administrator=True)
    async def verify_teacher(self, ctx, member: discord.Member):
        try:
            teacher_role = discord.utils.get(ctx.guild.roles, name="Teacher")

            if not teacher_role:
                teacher_role = await ctx.guild.create_role(name="Teacher")

            await member.add_roles(teacher_role)
            await self.verify_member(member)
            await ctx.send(f"{ctx.author.mention}, the role 'Teacher' has been given to {member.mention}.")
        except Exception as error:
            await ctx.send(f"{ctx.author.mention} An error occurred: {error}, please try report it and try again later")
            traceback.print_exc()


    






def setup(bot):  
    bot.add_cog(Verification(bot))