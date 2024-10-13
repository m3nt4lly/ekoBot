from bot.core import Bot, db
from discord import Interaction, Embed


@Bot.tree.command(description="Топ игроков")
async def leaderboard(inter: Interaction):
    session = db.Session()
    top_5 = session.query(db.Users).filter_by(guild_id=inter.guild.id).order_by(db.Users.lvl.desc()).limit(5).all()
    top_5_text = "\n".join(f"> {i}. {Bot.get_user(player.user_id).mention} - `{player.lvl}` уровень" for i, player in enumerate(top_5, start=1))
    embed = Embed(title="Топ игроков", description=top_5_text, color=0xff9900)
    await inter.response.send_message(embed=embed)
