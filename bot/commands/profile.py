import discord

from bot.core import Bot, db
from discord import Interaction

from ..config.cfg_manager import Config


@Bot.tree.command(description="Профиль пользователя.")
async def profile(inter: Interaction, user: discord.User = None):
    session = db.Session()
    if Config(inter.guild.id).check_economy_values() is False:
        await inter.response.send_message(embed=discord.Embed(description="На сервере не настроена экономика, обратитесь к администратору.", colour=discord.Colour.from_rgb(255, 153, 0)))
        session.close()
        return

    if user is None:
        user = inter.user

    xp = session.query(db.Users).filter_by(user_id=user.id, guild_id=inter.guild.id).value(db.Users.xp)
    lvl = session.query(db.Users).filter_by(user_id=user.id, guild_id=inter.guild.id).value(db.Users.lvl)
    money = session.query(db.Users).filter_by(user_id=user.id, guild_id=inter.guild.id).value(db.Users.money)

    embed = discord.Embed(colour=discord.Colour.from_rgb(255, 153, 0))
    embed.set_author(name=f"Профиль {user.name} ({user.id})", icon_url=user.display_avatar)
    embed.add_field(name="Опыт", value=f"{xp}/{int((Config(inter.guild.id).get_value('xp_for_new_lvl') * lvl) ** Config(inter.guild.id).get_value('multiplier'))}", inline=True)
    embed.add_field(name="Уровень", value=f"{lvl}", inline=True)
    embed.add_field(name="Коины", value=f"{money} ", inline=True)

    await inter.response.send_message(embed=embed)

    session.close()
