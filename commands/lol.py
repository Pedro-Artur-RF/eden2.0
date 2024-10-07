from discord.ext import commands
import requests, discord

def get_account_details(game_name, tag_line):
    # Substitua 'YOUR_API_KEY' pela sua chave de API da Riot
    api_key = ''
    
    # Obter PUUID
    response = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={api_key}")
    if response.status_code != 200:
        return None
    puuid = response.json()['puuid']
    
    # Obter ID e nível da conta
    summoner_response = requests.get(f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}')
    if summoner_response.status_code != 200:
        return None
    summoner_data = summoner_response.json()
    summoner_id = summoner_data['id']
    account_level = summoner_data['summonerLevel']
    profile_icon_id = summoner_data['profileIconId']
    
    # Inicializar variáveis de classificação
    rank_solo = division_solo = victory_solo = losses_solo = leaguePoints_solo = 0
    rank_flex = division_flex = victory_flex = losses_flex = leaguePoints_flex = 0
    
    # Obter dados de classificação para Solo/Duo e Flex
    rank_response = requests.get(f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}')
    if rank_response.status_code != 200:
        return None
    
    for entry in rank_response.json():
        if entry['queueType'] == 'RANKED_SOLO_5x5':
            rank_solo = entry['tier']
            division_solo = entry['rank']
            victory_solo = entry['wins']
            losses_solo = entry['losses']
            leaguePoints_solo = entry['leaguePoints']
        elif entry['queueType'] == 'RANKED_FLEX_SR':
            rank_flex = entry['tier']
            division_flex = entry['rank']
            victory_flex = entry['wins']
            losses_flex = entry['losses']
            leaguePoints_flex = entry['leaguePoints']
    
    # Obter a URL do ícone de invocador usando Data Dragon
    icon_url = f'http://ddragon.leagueoflegends.com/cdn/14.11.1/img/profileicon/{profile_icon_id}.png'
    
    return{
        'puuid': puuid,
        'summoner_id': summoner_id,
        'account_level': account_level,
        'rank_solo': rank_solo,
        'division_solo': division_solo,
        'victory_solo': victory_solo,
        'losses_solo': losses_solo,
        'leaguePoints_solo': leaguePoints_solo,
        'rank_flex': rank_flex,
        'division_flex': division_flex,
        'victory_flex': victory_flex,
        'losses_flex': losses_flex,
        'leaguePoints_flex': leaguePoints_flex,
        'icon_url': icon_url
    }

@commands.command()
async def lol(ctx, game_name: str, tag_line: str):
    account_details = get_account_details(game_name, tag_line)
    if account_details:
        winrate_solo = 0
        winrate_flex = 0
        if account_details['victory_solo'] + account_details['losses_solo'] > 0:
            winrate_solo = (account_details['victory_solo'] / (account_details['victory_solo'] + account_details['losses_solo'])) * 100
        if account_details['victory_flex'] + account_details['losses_flex'] > 0:
            winrate_flex = (account_details['victory_flex'] / (account_details['victory_flex'] + account_details['losses_flex'])) * 100

        embed = discord.Embed(title= f"{game_name}#{tag_line}", description=f"{account_details['account_level']}", color= discord.Color.red())
        embed.add_field(name="Solo/Duo", value= f"{account_details['rank_solo']} {account_details['division_solo']}")
        embed.set_thumbnail(url=account_details['icon_url'])
        await ctx.send(embed=embed)
    else:
        await ctx.send("Não foi possível receber os dados do invocador")

async def setup(bot):
    bot.add_command(lol)
