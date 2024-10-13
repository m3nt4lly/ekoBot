import discord

from bot.config.cfg_manager import Config
from bot.core.economy import check_lvl
from bot.core import db, Bot
from datetime import datetime
import random


async def check_voice_channels():
    await check_lvl(vc=True)


async def check_contests():
    session = db.Session()
    for guild in Bot.guilds:
        if Config(guild.id).check_contest_values() is False:
            continue

        current_time = datetime.now()

        contests = session.query(db.Contests).filter_by(guild_id=guild.id).all()

        for contest in contests:
            duration = contest.duration
            amount = contest.amount
            message_id = contest.message_id
            guild_id = contest.guild_id

            end_time = duration

            if current_time >= end_time:
                channel = Bot.get_channel(Config(guild_id).get_value('contest_channel_id'))
                message = await channel.fetch_message(message_id)

                reactions = message.reactions
                participants = []

                for reaction in reactions:
                    async for user in reaction.users():
                        if not user.bot:
                            participants.append(user)

                if participants:
                    winner = random.choice(participants)
                    session.query(db.Users).filter_by(user_id=winner.id, guild_id=guild_id).update({db.Users.money: db.Users.money + amount})
                    embed = discord.Embed(description=f"Сумма выигрыша: `{amount}` коинов.", colour=discord.Colour.green())
                    embed.set_author(name=f"Победитель розыгрыша: {winner.name} ({winner.id})", icon_url=winner.avatar.url)
                    await message.edit(embed=embed)
                else:
                    await message.delete()

                session.delete(contest)
                session.commit()

    session.close()
