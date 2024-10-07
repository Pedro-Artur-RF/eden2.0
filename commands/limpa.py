from discord.ext import commands


@commands.has_permissions(manage_messages=True)
@commands.command()
async def limpa(ctx, num: int):
    if num <= 100:
        await ctx.channel.purge(limit=num+1)
    else:
        await ctx.send("Tá de sacanagem fdp? ", num, " é mto")
@limpa.error
async def check_manage_messages_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, você não tem permissão pra isso :3")

async def setup(bot):
    bot.add_command(limpa)
