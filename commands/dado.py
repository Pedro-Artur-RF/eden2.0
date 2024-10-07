from discord.ext import commands
import random, re

@commands.command()
async def dado(ctx, *, arg:str):
    # Usa expressão regular para encontrar números, lados e bônus
    match = re.match(r'(\d+)d(\d+)([+-]\d+)?', arg)
    if match:
        num1 = int(match.group(1))
        num2 = int(match.group(2))
        bonus = int(match.group(3)) if match.group(3) else 0
        total = 0
        results = []
        
        for _ in range(num1):
            rolagem_original = random.randint(1, num2)
            rolagem_com_bonus = rolagem_original + bonus
            results.append((rolagem_original, rolagem_com_bonus))
            total += rolagem_com_bonus
        
        results_str = ', '.join(f"{original}->({com_bonus})" for original, com_bonus in results)
        await ctx.send(f"```{results_str}```")
    else:
        await ctx.send("Por favor, use o formato correto: !dado <número de dados>d<lados do dado>[+<bônus>]")

async def setup(bot):
    bot.add_command(dado)