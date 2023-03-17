import discord
from pyfaceit import Pyfaceit

intents = discord.Intents.default()
client = discord.Client(intents=intents)
token = 'YOURTOKEN'
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="statistics"))
    

@tree.command(name="stats", description="Get faceit player's statistics")
async def faceit(interaction, nickname: str):
    try:
        await interaction.response.defer()
        stats = Pyfaceit(nickname).player_stats()
        info = Pyfaceit(nickname).player_information()
        stats_lifetime = dict(stats.get("lifetime"))
        flag = info.get("country")
        avatar = info.get("avatar")
        matches = stats_lifetime.get("Matches")
        wins = stats_lifetime.get("Wins")
        kd = stats_lifetime.get("Average K/D Ratio")
        headshots_percent = stats_lifetime.get("Average Headshots %")
        longest_win_streak = stats_lifetime.get("Longest Win Streak")
        temp_recent_results = stats_lifetime.get("Recent Results")
        recent_results = ""
        for i in temp_recent_results:
            if i == "0":
                recent_results += "L"
            if i == "1":
                recent_results += "W"
            recent_results += " "
        recent_results = recent_results[:-1]
        emb = discord.Embed(title=nickname + " :flag_" + flag + ":", description=
        "Matches: " + matches
        + "\nWins: " + wins
        + '\n'
        + "\nK/D: " + kd
        + "\nHeadshots %: " + headshots_percent
        + '\n'
        + "\nLongest wnstreak: " + longest_win_streak
        + "\nRecent results: " + recent_results, colour=discord.Colour.orange())
        emb.set_image(url=avatar)
        await interaction.followup.send(embed=emb)
    except:
        emb = discord.Embed(title=nickname, description="Faceit profile with this nickname doesn't exist",
                            colour=discord.Colour.red())
        emb.set_image(url="https://i.imgur.com/F8KwoyM.png")
        await interaction.followup.send(embed=emb)


@tree.command(name="elo", description="Get faceit player's elo")
async def faceit(interaction, nickname: str):
    try:
        await interaction.response.defer()
        info = Pyfaceit(nickname).player_information()
        info_games_csgo = dict(info.get("games")).get("csgo")
        flag = info.get("country")
        avatar = info.get("avatar")
        level = info_games_csgo.get("skill_level")
        if (level == 1):
            level_emoji = ":white_circle:"
        if (level == 2 or level == 3):
            level_emoji = ":green_circle:"
        if (level == 4 or level == 5 or level == 6 or level == 7):
            level_emoji = ":yellow_circle:"
        if (level == 8 or level == 9):
            level_emoji = ":orange_circle:"
        if (level == 10):
            level_emoji = ":red_circle:"
        elo = info_games_csgo.get("faceit_elo")
        emb = discord.Embed(title=nickname + " :flag_" + flag + ":", description=
        level_emoji + " Level " + str(level)
        + '\n' + level_emoji + " Elo: " + str(elo), colour=discord.Colour.orange())
        emb.set_image(url=avatar)
        await interaction.followup.send(embed=emb)
    except:
        emb = discord.Embed(title=nickname, description="Faceit profile with this nickname doesn't exist",
                            colour=discord.Colour.red())
        emb.set_image(url="https://i.imgur.com/F8KwoyM.png")
        await interaction.followup.send(embed=emb)


client.run(token)
