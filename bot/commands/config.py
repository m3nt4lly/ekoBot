from typing import List

from discord.ext import commands

from bot.core import Bot
from discord import Interaction, app_commands
from ..config.cfg_manager import Config

column_ = ['xp_for_new_lvl', 'blacklist_channel_ids', 'afk_channel_ids', 'vc_channel_notification', 'multiplier', 'lvl5', 'lvl10', 'lvl15', 'lvl20', 'lvl20plus', 'contest_channel_id']


@Bot.tree.command(description="Настроить КФГ сервера.")
@commands.has_permissions(administrator=True)
async def config(inter: Interaction, column: str, value: str):
    cfg = Config(inter.guild.id)
    if column == 'blacklist_channel_ids' or column == 'afk_channel_ids':
        value = [int(x) for x in value.split(', ')]
    cfg.set_value(column, value)
    await inter.response.send_message(f"Значение `{column}` изменено на `{value}`", ephemeral=True)


@Bot.tree.command(description="Показать настройки сервера.")
@commands.has_permissions(administrator=True)
async def show_config(inter: Interaction):
    cfg = Config(inter.guild.id)
    embed = cfg.create_embed()
    await inter.response.send_message(embed=embed, ephemeral=True)


@config.autocomplete("column")
async def config_autocomplete(inter: Interaction, current: str) -> List[app_commands.Choice[str]]:
    raw_data = column_[:]
    cfg = Config(inter.guild.id)

    to_remove = []

    for item in raw_data:
        value = cfg.get_value(item)
        if cfg.check_economy_values():
            break

        if value is not None:
            to_remove.append(item)

    filtered_data = [item for item in raw_data if item not in to_remove]

    data = []
    for choice in filtered_data:
        if current.lower() in choice.lower():
            data.append(app_commands.Choice(name=choice, value=choice))
    return data


