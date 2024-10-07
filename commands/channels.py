import discord
from discord.ext import commands

@commands.command()
async def channels(ctx, *,server_name: str):
    # Find the server by name
    server = discord.utils.get(commands.guilds, name=server_name)
    if not server:
        await ctx.send(f"Server '{server_name}' não encontrado")
        return

    # Create an embed to display channel information
    embed = discord.Embed(title=f"Canais em: {server.name}", color=discord.Color.blue())
    for channel in server.text_channels:
        embed.add_field(name=channel.name, value=f"ID: {channel.id}", inline=False)
    await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(channels)