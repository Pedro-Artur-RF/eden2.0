from discord.ext import commands

@commands.command()
async def oioi(ctx):
    await ctx.send(f'oioi seu gay {ctx.author.display_name}.')


async def setup(bot):
    bot.add_command(oioi)