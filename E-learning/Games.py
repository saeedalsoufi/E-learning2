import discord
from discord.ext import commands
import random 
from Database import Database


db = Database('Game_Points.db')

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description = "This is a rock paper scissors game vs the bot.")
    async def rps(self, ctx):
        rpsGame = ['rock', 'paper', 'scissors']
        await ctx.send(f"{ctx.author.mention} Rock, paper, or scissors? Choose wisely...")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

        user_choice = await self.bot.wait_for('message', check=check)
        user_choice_text = user_choice.content.lower()  # Get the user choice text and convert it to lowercase

        comp_choice = random.choice(rpsGame)
        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)

        winner = None
        if user_choice_text == comp_choice:
            winner = None
        elif (user_choice_text == "rock" and comp_choice == "scissors") or (user_choice_text == "paper" and comp_choice == "rock") or (user_choice_text == "scissors" and comp_choice == "paper"):
            winner = ctx.author
            db.add_point(server_id, user_id)
        else:
            winner = "bot"
            db.remove_point(server_id, user_id)

        if winner == ctx.author:
            await ctx.send(f"Congratulations {ctx.author.mention}, you won!\nYour choice: {user_choice_text}\nMy choice: {comp_choice}")
        elif winner == "bot":
            await ctx.send(f"{ctx.author.mention}, I won this round!\nYour choice: {user_choice_text}\nMy choice: {comp_choice}")
        else:
            await ctx.send(f"{ctx.author.mention}, it's a tie!\nYour choice: {user_choice_text}\nMy choice: {comp_choice}")


    @commands.command(description = "This is a fighting game vs the bot, you and your bot will deal a random damage from 0 to 100.")
    async def fight(self, ctx):
        damageDealt = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']

        user_damage = random.choice(damageDealt)
        comp_damage = random.choice(damageDealt)
        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)

        winner = None
        if user_damage == comp_damage:
            winner = None
        elif (user_damage == "10%" and comp_damage in damageDealt[1:9]) or (user_damage == "20%" and comp_damage in damageDealt[2:9]) \
                or (user_damage == "30%" and comp_damage in damageDealt[3:9]) or (user_damage == "40%" and comp_damage in damageDealt[4:9]) \
                or (user_damage == "50%" and comp_damage in damageDealt[5:9]) or (user_damage == "60%" and comp_damage in damageDealt[6:9]) \
                or (user_damage == "70%" and comp_damage in damageDealt[7:9]) or (user_damage == "80%" and comp_damage in damageDealt[8:9]) \
                or (user_damage == "90%" and comp_damage in damageDealt[9]):
            winner = "bot"
            db.remove_point(server_id, user_id)
        else:
            winner = ctx.author
            db.add_point(server_id, user_id)

        if winner == ctx.author:
            await ctx.send(f"Congratulations {ctx.author.mention}, you won!\nYour hit dealt {user_damage} damage to my health\nMy hit dealt {comp_damage} to your health")
        elif winner == "bot":
            await ctx.send(f"{ctx.author.mention}, I won this round!\nYour hit dealt {user_damage} damage to my health\nMy hit dealt {comp_damage} to your health")
        else:
            await ctx.send(f"{ctx.author.mention}, it's a tie!\nWe have both dealt {user_damage} to eachother")



    @commands.command(description = "This command will list the amount of points the user have gained from his ratio of winning games.")
    async def listpoints(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        server_id = str(ctx.guild.id)
        user_id = str(member.id)

        points = db.get_points(server_id, user_id)

        if points is None:
            await ctx.send(f"{member.display_name} has no gaming points.")
        else:
            await ctx.send(f"{member.display_name} has {points} gaming points.")

def setup(bot):
    bot.add_cog(Games(bot))



