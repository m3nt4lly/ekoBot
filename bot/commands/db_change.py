from typing import Literal

import discord

from bot.core import Bot, db
from discord import Interaction

from discord.ext import commands


@Bot.tree.command(description="Изменить значения базы данных.")
@commands.has_permissions(administrator=True)
async def db_change(inter: Interaction, user: discord.Member, value: str,
                    column: Literal['lvl', 'money', 'xp']):
    session = db.Session()
    session.query(db.Users).filter_by(user_id=user.id, guild_id=user.guild.id).update({column: value})
    session.commit()
    session.close()
    await inter.response.send_message(
        embed=discord.Embed(description=f"Значение {column} пользователя {user.mention} изменено на {value}.",
                            colour=discord.Colour.from_rgb(68, 148, 74)))
