import uuid

from disnake import Color, Embed

from cogs.buttons import lol, overwatch, valorant
from core.embeds import error


def region_icon(region, game):
    if game == "lol":
        if region == "euw":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1075444853028175934/OW_Europe.png"
        elif region == "eune":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1075444853028175934/OW_Europe.png"
        elif region == "br":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1075444852579373136/OW_Americas.png"
        elif region == "la":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1075444852579373136/OW_Americas.png"
        elif region == "jp":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1075444853233684581/VAL_AP.png"
        elif region == "las":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1075444852579373136/OW_Americas.png"
        elif region == "tr":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1075444853233684581/VAL_AP.png"
        elif region == "oce":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1075444853233684581/VAL_AP.png"
        elif region == "ru":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1075444853233684581/VAL_AP.png"
        else:
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1075444852369670214/VAL_NA.png"

    elif game == "valorant":
        if region == "ap":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1077957848161591387/VAL_AP.png"
        elif region == "br":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1077957848409067661/VAL_BR.png"
        elif region == "kr":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1077957848660713494/VAL_KR.png"
        elif region == "latam":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1077957848899801129/VAL_LATAM.png"
        elif region == "na":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1077957849130467408/VAL_NA.png"
        else:
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1077959248853598308/IMG_6379.png"

    else:
        if region == "americas":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1077957898329673728/OW_Americas.png"
        elif region == "asia":
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1077957898598101022/OW_Asia.png?width=572&height=572"
        else:
            icon_url = "https://media.discordapp.net/attachments/1046664511324692520/1077957898963013814/OW_Europe.png"

    return icon_url

def banner_icon(game):
    if game == "lol":
        return "https://cdn.discordapp.com/attachments/328696263568654337/1068133100451803197/image.png"
    elif game == "valorant":
        return "https://media.discordapp.net/attachments/1046664511324692520/1077958380964036689/image.png"
    else:
        return "https://media.discordapp.net/attachments/1046664511324692520/1077958380636868638/image.png"

def get_title(game):
    if game == "lol":
        return "Match Overview - SR Tournament Draft"
    elif game == "valorant":
        return "Match Overview - Valorant Competitive"
    else:
        return "Match Overview - Overwatch Competitive"

async def start(bot, channel, game, author=None):
    data = await bot.fetchrow(
        f"SELECT * FROM queuechannels WHERE channel_id = {channel.id}"
    )
    if not data:
        try:
            return await channel.send(
                embed=error(
                    f"{channel.mention} is not setup as the queue channel, please run this command in a queue channel."
                )
            )
        except:
            if author:
                return await author.send(embed=error(f"Could not send queue in {channel.mention}, please check my permissions."))

    # If you change this - update /events.py L28 as well!
    title = get_title(game)
    embed = Embed(
        title=title, color=Color.red()
    )
    st_pref = await bot.fetchrow(f"SELECT * FROM switch_team_preference WHERE guild_id = {channel.guild.id}")
    if not st_pref:
        embed.add_field(name="Slot 1", value="No members yet")
        embed.add_field(name="Slot 2", value="No members yet")
    else:
        embed.add_field(name="🔵 Blue", value="No members yet")
        embed.add_field(name="🔴 Red", value="No members yet")
    if channel.guild.id == 1071099639333404762:
        embed.set_image(url="https://media.discordapp.net/attachments/1071237723857363015/1073428745253290014/esporty_banner.png")
    else:
        banner = banner_icon(game)
        embed.set_image(url=banner)
    embed.set_footer(text=str(uuid.uuid4()).split("-")[0])
    if not data[1]:
        data = (data[0], 'na')
    icon_url = region_icon(data[1], game)
    
    embed.set_author(name=f"{data[1].upper()} Queue", icon_url=icon_url)
    
    if game == "lol":
        button = lol
    elif game == "valorant":
        button = valorant
    else:
        button = overwatch
    
    try:
        await channel.send(embed=embed, view=button.QueueButtons(bot))
    except:
        if author:
            await author.send(embed=error(f"Could not send queue in {channel.mention}, please check my permissions."))