import discord
from pyfaceit import Pyfaceit

intents = discord.Intents.default()
client = discord.Client(intents=intents)
token = 'YOURTOKEN'
server_id = 'YOURSERVERID'
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="бот от злого грифера"))
    print("Ready")

@tree.command(name = "faceit", description = "Get faceit profile", guild=discord.Object(id=server_id))
async def faceit(interaction, nickname: str):
    try:
        stats = Pyfaceit(nickname).player_stats()
        stats_lifetime = dict(stats.get("lifetime"))
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
        emb = discord.Embed(title=nickname, description=
        "Matches: " + matches
        + "\nWins: " + wins
        + '\n'
        + "\nK/D: " + kd
        + "\nHeadshots %: " + headshots_percent
        + '\n'
        + "\nLongest wnstreak: " + longest_win_streak
        + "\nRecent results: " + recent_results, colour=discord.Colour.orange())
        emb.set_image(url="https://i.imgur.com/UrloakJ.png")
        await interaction.response.send_message(embed=emb)
    except:
        emb = discord.Embed(title=nickname, description="Faceit profile with this nickname doesn't exist", colour=discord.Colour.red())
        emb.set_image(url="https://i.imgur.com/F8KwoyM.png")
        await interaction.response.send_message(embed=emb)

client.run(token)
