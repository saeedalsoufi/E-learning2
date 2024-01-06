import discord
from discord.ext import commands
from discord.ext.commands.core import group
from Database import Database
import sqlite3 
import traceback

class DatabaseCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database('Classes.db')



    #This command will create a class in the database which will contain teahcers usernames and students. It will also create a new category in the server containing-
    #A text channel and a voice-channel who can be accesed only by the class members.
    @commands.command(description="This will create a class for you which will create a private category for the teachers and students you will choose.")
    @commands.has_permissions(administrator=True)
    async def createclass(self, ctx):
        server_id = str(ctx.guild.id)
        try:
            await ctx.send(f"{ctx.author.mention} What is the name of the class you would like to create?")
            class_name = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)

            # Create a new role for the class.
            role = await ctx.guild.create_role(name=class_name.content, mentionable=True)
            #Create a new category with it's channels for the class.
            category = await ctx.guild.create_category(class_name.content)
            text_channel = await category.create_text_channel(f"{class_name.content.lower()}-text")
            voice_channel = await category.create_voice_channel(f"{class_name.content.lower()}-voice")

            await ctx.send(f"{ctx.author.mention} Please list the usernames of the teachers that you would like in the {class_name.content} class? (Please separate each teacher with a space, or reply 'empty' if you don't want to add teachers now')")
            teachers = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            teachers_usernames = teachers.content.strip().lower()
            teacher_mentions = []
            if teachers_usernames == 'empty':
                teachers_usernames = ''
            else:
                teachers_usernames = ", ".join([teacher.mention for teacher in teachers.mentions])
                teacher_mentions = teachers.mentions

            await ctx.send(f"{ctx.author.mention} Please list the usernames of the students that you would like in the {class_name.content} class? (Please separate each student with a space, or reply 'empty' if you don't want to add students now')")
            students = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            students_usernames = students.content.strip().lower() 
            student_mentions = []
            if students_usernames == 'empty':
                students_usernames = ''
            else:
                students_usernames = ", ".join([student.mention for student in students.mentions])
                student_mentions = students.mentions

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True, connect=True),
                role: discord.PermissionOverwrite(read_messages=True, connect=True)  
            }

            # This will make the new created channels for the class private for the class teachera
            await text_channel.edit(overwrites=overwrites)
            await voice_channel.edit(overwrites=overwrites)

            # Assign the new role to all the teachers and students that's been collected from the user.
            for teacher in teacher_mentions:
                await teacher.add_roles(role)

            for student in student_mentions:
                await student.add_roles(role)

            # This will create the class in the database with the chosen class name and then add the students and teachers 
            self.database.createclass(server_id, class_name.content, teachers_usernames, students_usernames)
            await ctx.send(f"{ctx.author.mention} Teachers: {teachers_usernames}\nStudents: {students_usernames}\nThe teachers and students above have been added to '{class_name.content}' and assigned the '{role.name}' role.")

        except sqlite3.IntegrityError:
            await ctx.send(f"{ctx.author.mention} This class name '{class_name.content}' already exists. Please choose another name and try again.")



    #This function 
    @commands.command(description= "Please write the class name you want to edit like this ?editclass classname")
    @commands.has_permissions(administrator=True)
    async def editclass(self, ctx, class_name):
        try:
            server_id = str(ctx.guild.id)
            existing_class = self.database.getclass(server_id, class_name)
            if existing_class is None:
                await ctx.send(f"{ctx.author.mention} This class does not exist.")
                return

            # This will ask the user if he wants to edit the list of students or teachers in the class
            await ctx.send(f"{ctx.author.mention} Please choose which list you would like to change by typing: 'students' or 'teachers'.")
            action = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
            action = action.content.strip().lower()

            if action not in ['students', 'teachers']:
                await ctx.send(f"{ctx.author.mention} Invalid input. Please type either 'students' or 'teachers'.")
                return

            # Now we will ask the user for the new list of usernames for the teachers/students
            await ctx.send(f"{ctx.author.mention} Please list the new user IDs of the {action} that you would like to add or remove, separated by spaces. (Type 'cancel' to cancel)")
            users = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
            user_mentions = []
            if users.content.strip().lower() != 'cancel':
                user_mentions = users.mentions

            updated_fields = {action: ", ".join([user.mention for user in user_mentions])}
            self.database.editclass(server_id, class_name, updated_fields)

            # Find the corresponding category in the server
            category = None
            for cat in ctx.guild.categories:
                if cat.name.lower() == class_name.lower():
                    category = cat
                    break

            if category:
                # Update the permissions for the text and voice channels
                text_channel = None
                voice_channel = None
                for channel in category.channels:
                    if channel.type == discord.ChannelType.text and channel.name == f"{class_name.lower()}-text":
                        text_channel = channel
                    elif channel.type == discord.ChannelType.voice and channel.name == f"{class_name.lower()}-voice":
                        voice_channel = channel

                if text_channel and voice_channel:
                    overwrites = text_channel.overwrites
                    for user in user_mentions:
                        overwrites[user] = discord.PermissionOverwrite(read_messages=True, connect=True)

                    await text_channel.edit(overwrites=overwrites)
                    await voice_channel.edit(overwrites=overwrites)

            await ctx.send(f"{ctx.author.mention} The list of {action} for '{class_name}' has been updated.")
        except Exception as error:
            await ctx.send(f"{ctx.author.mention} An error occurred: {error}, please try report it and try again later")
            traceback.print_exc()




    @commands.command(description= "This will list all the classes that you have created")
    @commands.has_permissions(administrator=True)
    async def listclasses(self, ctx):
        try:
            server_id = str(ctx.guild.id)
            classes = self.database.listclasses(server_id)
            #This will check if there is any class that exist in the server
            if len(classes) == 0:
                await ctx.send("{ctx.author.mention} There are no classes for this server.")
            else:
                response = "List of classes:\n"
                for row in classes:
                    class_name = row[0]
                    teachers_row = row[1]
                    students_row = row[2]
                    teacher_usernames = []
                    student_usernames = []
                    if teachers_row:
                        teacher_ids = teachers_row.split(",")
                        for teacher_id in teacher_ids:
             
                            teacher_id = teacher_id.strip("<@>")
                            teacher = await ctx.guild.fetch_member(int(teacher_id))
                            if teacher:
                                teacher_usernames.append(teacher.mention)
                    if students_row:
                        student_ids = students_row.split(",")
                        for student_id in student_ids:
                    
                            student_id = student_id.strip("<@>")
                            student = await ctx.guild.fetch_member(int(student_id))
                            if student:
                                student_usernames.append(student.mention) 
                                    #This is a common way to format the way the class and students and teachers are being displayed:
                    response += f"{class_name}:\nTeachers: {' '.join(teacher_usernames) if teacher_usernames else 'empty'}\nStudents: {' '.join(student_usernames) if student_usernames else 'empty'}\n\n"
                await ctx.send(response)
        except Exception as error:
            await ctx.send(f"{ctx.author.mention} An error occurred: {error}, please try report it and try again later")
            traceback.print_exc()

    @commands.command(description= "Please write the class name you want to delete like this ?deleteclass classname")
    @commands.has_permissions(administrator=True)
    async def deleteclass(self, ctx, class_name: str):
        try:
            server_id = str(ctx.guild.id)

            group = self.database.getclass(server_id, class_name)
            if not group:
                await ctx.send(f"{ctx.author.mention} This class '{class_name}' does not exist. Please enter a valid class name that exists.")
                return

            role = discord.utils.get(ctx.guild.roles, name=class_name)

            if role:
                for member in role.members:
                    await member.remove_roles(role)
                await role.delete()

            self.database.conn.execute("DELETE FROM classes WHERE server_id = ? AND class_name = ?", (server_id, class_name))
            self.database.conn.commit()

            for category in ctx.guild.categories:
                if category.name.lower() == class_name.lower():
                    for channel in category.channels:
                        await channel.delete()

                    # Then, delete the category itself
                    await category.delete()
                    await ctx.send(f"{ctx.author.mention} The class '{class_name}' has been deleted from the database and the channels have been deleted from the server'.")
                    break
            else:
                await ctx.send(f"{ctx.author.mention} The class '{class_name}' has been deleted from the database, but its channels couldn't be found in the server.")
        except Exception as error:
            await ctx.send(f"{ctx.author.mention} An error occurred: {error}, please try report it and try again later")
            traceback.print_exc()

#Add the commands of this cog to the bot
def setup(bot): 
    bot.add_cog(DatabaseCommands(bot))
