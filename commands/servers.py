import discord
from discord.ext import commands

@commands.command()
async def servers(ctx):
    embed = discord.Embed(title="Lista de Servidores", color=discord.Color.blue())
    for guild in commands.bot.guilds:
        embed.add_field(name=f"{guild.name}[{len(guild.text_channels)}]", value=f"ID:{guild.id}", inline=False)
    await ctx.send(embed)

async def setup(bot):
    bot.add_command(servers)