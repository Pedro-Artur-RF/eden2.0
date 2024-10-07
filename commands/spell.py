import discord, json
from discord.ext import commands

@commands.command()
async def spell(ctx, *, spellName:str):
    
    with open(f'./spells/{spellName.replace(" ", "-").casefold()}.json') as json_file:
        spellData = json.load(json_file)

    embed = discord.Embed(title=spellData['name'])

    for key, value in spellData['system'].items():
        if value and isinstance(value, dict):
            for subkey, subvalue in value.items():
                if subvalue:
                    embed.add_field(name=f"{key.capitalize()} - {subkey.capitalize()}", value=subvalue, inline=False)
        elif value:
            embed.add_field(name=key.capitalize(), value=value, inline=False)

    await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(spell)