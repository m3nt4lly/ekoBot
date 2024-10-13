import discord

from bot.core import Bot
from discord import Interaction

from ..config.cfg_manager import Config


@Bot.tree.command(description="Информация о боте.")
async def about(inter: Interaction):
    economy_message, contest_message = "```ansi\n[2;32mНАСТРОЕНА[0m\n```", "```ansi\n[2;32mНАСТРОЕНЫ[0m\n```"
    if Config(inter.guild.id).check_economy_values() is False:
        economy_message = "```ansi\n[2;31mНЕ НАСТРОЕНА[0m[2;31m[0m\n```"
    if Config(inter.guild.id).check_contest_values() is False:
        contest_message = "```ansi\n[2;31mНЕ НАСТРОЕНЫ[0m[2;31m[0m\n```"
    embed = discord.Embed(title="О боте", color=discord.Colour.from_rgb(255, 153, 0),
                          description="Данный бот специализируется на экономике. Для первичной настройки воспользуйтесь командой `/config`")
    embed.add_field(name="Экономика", value=economy_message, inline=False)
    embed.add_field(name="Розыгрыши", value=contest_message, inline=False)
    await inter.response.send_message(embed=embed)
