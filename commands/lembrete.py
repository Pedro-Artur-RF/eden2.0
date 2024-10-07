from discord.ext import commands
import datetime, asyncio

@commands.command()
async def lembrete(ctx, tempo: str, *, lembrete: str):
    h, m, s = tempo.split(':')
    tempo_em_segundos = int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())
    await ctx.send(f"Ok, em {tempo}, te lembrarei de {lembrete} :3")
    
    # Aguarda o tempo especificado sem bloquear o loop de eventos
    await asyncio.sleep(tempo_em_segundos)
    
    # Envia a mensagem de lembrete após o tempo de espera
    await ctx.send(f'Hey {ctx.author.mention}, não se esqueça de: {lembrete}!')

async def setup(bot):
    bot.add_command(lembrete)