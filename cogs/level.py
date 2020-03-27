import discord
from discord.ext import commands

from utility import LevelsQuery, ranking, IdPing

client = commands.Bot(command_prefix="$")

class level(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="level", aliases=["levelquery","rank"], description="returns your level or another members level requires ping.")
    async def UserLevelQuery(self, ctx, user:discord.User=None):
        async with ctx.channel.typing():
            if user is None:
                usrid = ctx.author.id
                user = ctx.author
            else:
                usrid = user.id
            QueryResult = await LevelsQuery(usrid)
            try:
                XP = QueryResult[0][0]
                lvl = QueryResult[0][1]
                rank = QueryResult[0][2]
                embed = discord.Embed(title=f"{user.name} level info", description=f"**Rank**: {rank}\n**lvl**: {lvl}\n**XP**: {XP}", colour=discord.Color.dark_blue())
                await ctx.send(embed=embed)
            except TypeError:
                await ctx.send(f"{user.name} is unranked!")
        return None
        
    @commands.command(name="leaderboard", aliases=["lb"], description="gives the leaderboard, can be used as $lb")
    async def leaderboard(self, ctx):
        async with ctx.channel.typing():
            users = [f'{str(i[0])}]{str(i[1])}' for i in list(enumerate(await ranking(10), start=1))]
            embed = discord.Embed(title="Leaderboard", colour=discord.Color.dark_blue())
            #embed.add_field(name="rank", value=str("\n".join(series)), inline=True)
            embed.add_field(name="user", value=str("\n".join(users)), inline=True)
            await ctx.send(embed=embed, content=None)
        
def setup(client):
    client.add_cog(level(client))
