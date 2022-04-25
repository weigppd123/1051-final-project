import discord
import json
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError


IRON =          'https://static.wikia.nocookie.net/leagueoflegends/images/f/fe/Season_2022_-_Iron.png/revision/latest/scale-to-width-down/1000?cb=20220105213520'
BRONZE =        'https://static.wikia.nocookie.net/leagueoflegends/images/e/e9/Season_2022_-_Bronze.png/revision/latest/scale-to-width-down/1000?cb=20220105214224'
SILVER =        'https://static.wikia.nocookie.net/leagueoflegends/images/4/44/Season_2022_-_Silver.png/revision/latest/scale-to-width-down/1000?cb=20220105214225'
GOLD =          'https://static.wikia.nocookie.net/leagueoflegends/images/8/8d/Season_2022_-_Gold.png/revision/latest/scale-to-width-down/1000?cb=20220105214225'
PLAT =          'https://static.wikia.nocookie.net/leagueoflegends/images/3/3b/Season_2022_-_Platinum.png/revision/latest/scale-to-width-down/1000?cb=20220105214225'
DIAMOND =       'https://static.wikia.nocookie.net/leagueoflegends/images/e/ee/Season_2022_-_Diamond.png/revision/latest/scale-to-width-down/1000?cb=20220105214226'
MASTER =        'https://static.wikia.nocookie.net/leagueoflegends/images/e/eb/Season_2022_-_Master.png/revision/latest/scale-to-width-down/1000?cb=20220105214311'
GRANDMASTER =   'https://static.wikia.nocookie.net/leagueoflegends/images/f/fc/Season_2022_-_Grandmaster.png/revision/latest/scale-to-width-down/1000?cb=20220105214312'
CHALLENGER =    'https://static.wikia.nocookie.net/leagueoflegends/images/0/02/Season_2022_-_Challenger.png/revision/latest/scale-to-width-down/1000?cb=20220105214312'


def getrank(tier):
    if(tier == 'IRON'):
        return IRON
    elif(tier == 'BRONZE'):
        return BRONZE
    elif(tier == 'SILVER'):
        return SILVER
    elif(tier == 'GOLD'):
        return GOLD
    elif(tier == 'PLATINUM'):
        return PLAT
    elif(tier == 'DIAMOND'):
        return DIAMOND
    elif(tier == 'MASTER'): 
        return MASTER
    elif(tier == 'GRANDMASTER'):
        return GRANDMASTER
    elif(tier == 'CHALLENGER'):
        return CHALLENGER


lol_watcher = LolWatcher('')
NA = 'NA1'

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("bot is ready")   

@client.command()
async def opgg(ctx, *, summonerName):

    account = lol_watcher.summoner.by_name(NA, summonerName)
    account_stats = lol_watcher.league.by_summoner(NA, account['id'])

    puuid = account['puuid']
    ign = account['name']
    summ = account['name']
    tier = account_stats[0]['tier']
    rank = account_stats[0]['rank']
    wins = account_stats[0]['wins']
    losses = account_stats[0]['losses']
    lp = account_stats[0]['leaguePoints']
    winrate = round((wins/(wins+losses))*100)
    
    if ' ' in ign:
        ign = ign.replace(" ", "%20")

    embed=discord.Embed(
        title = summ,
        description =   str(tier) + " " + str(rank) + "\n" + 
                        str(lp) + " LP  /  " + str(wins) + "W  " + str(losses) + "L\n" + 
                        "Win Rate " + str(winrate) + "%",
        url="https://na.op.gg/summoners/na/" + ign,
        color=discord.Color.blue()
    )
    embed.set_author(name="OP.GG", icon_url="https://pbs.twimg.com/profile_images/1258584949596119040/JJMKHIAg_400x400.jpg")
    embed.set_thumbnail(url=getrank(tier))

 
    match_list = lol_watcher.match.matchlist_by_puuid("americas", puuid, count=5, queue=420)
    for match in match_list:
        game = lol_watcher.match.by_id("americas", match)
        my_list = game['info']['participants']

       
        for player in my_list:
            if(player['summonerName'] == summ):
                if(player['win'] == True):
                    result = "Win"
                    champion = "**" + player['championName'] + "**"
                    results = str(player['kills']) + "/" + str(player['deaths']) + "/" + str(player['assists'])
                    embed.add_field(name=champion, value=results, inline=False)
                else:
                    result = "Loss"
                    champion = "~~" + player['championName'] + "~~"
                    results = str(player['kills']) + "/" + str(player['deaths']) + "/" + str(player['assists'])
                    embed.add_field(name=champion, value=results, inline=False)
        
    await ctx.send(embed=embed)

client.run('')
