import discord
from datetime import datetime, timedelta
from discord.utils import format_dt
from discord.ext import commands
from bot.config.cfg_manager import Config
from bot.core import Bot, db


class ContestModal(discord.ui.Modal, title='Создание розыгрыша'):
    def __init__(self):
        super().__init__()

    contest_value = discord.ui.TextInput(
        label="Сумма розыгрыша",
        placeholder="Сумма",
        custom_id="amount",
        style=discord.TextStyle.short,
    )

    contest_duration = discord.ui.TextInput(
        label="Длительность розыгрыша",
        placeholder="Пример: 1d, 5h, 30m",
        custom_id="duration",
        style=discord.TextStyle.short,
    )

    async def on_submit(self, inter: discord.Interaction):
        session = db.Session()
        try:
            duration = self.contest_duration.value
            value, unit = int(duration[:-1]), duration[-1]

            if unit == 'm':
                delta = timedelta(minutes=value)
            elif unit == 'h':
                delta = timedelta(hours=value)
            elif unit == 'd':
                delta = timedelta(days=value)
            else:
                raise ValueError("Invalid duration format")

            end_time = datetime.now() + delta

            embed = discord.Embed(colour=discord.Color.blurple())
            embed.set_author(name=f"Розыгрыш от администратора: {inter.user.name}", icon_url=inter.user.avatar.url)
            embed.add_field(name="Сумма", value=f"{self.contest_value.value} коинов", inline=False)
            embed.add_field(name="Закончится", value=format_dt(end_time, style='f'), inline=False)

            channel = Bot.get_channel(int(Config(inter.guild.id).get_value('contest_channel_id')))
            message = await channel.send(embed=embed)

            await message.add_reaction("👍")

            session.add(db.Contests(duration=end_time, amount=int(self.contest_value.value), message_id=message.id, guild_id=inter.guild.id))
            session.commit()
            await inter.response.send_message("Розыгрыш создан!", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Ошибка: {e}", ephemeral=True)
        finally:
            session.close()


@Bot.tree.command(description="Создать розыгрыш")
@commands.has_permissions(administrator=True)
async def contest(inter: discord.Interaction):
    await inter.response.send_modal(ContestModal())
