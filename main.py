from discord.ext import tasks
from bot.tasks.economy import *
from bot.tasks.database import *
from bot.tasks.economy import check_lvl
from bot.cfg import token
import bot.commands
import discord


@tasks.loop(minutes=10.0)
async def database_tasks():
    await update()


@tasks.loop(minutes=1.0)
async def economic_tasks():
    await check_voice_channels()
    await check_contests()


@Bot.event
async def on_member_join(member: discord.Member):
    session = db.Session()
    user = session.query(db.Users).filter_by(user_id=member.id, guild_id=member.guild.id).value(db.Users.user_id)
    if user is None:
        session.add(db.Users(guild_id=member.guild.id, user_id=member.id, name=member.name, lvl=1, xp=0, money=0))
        session.commit()
    else:
        pass

    session.close()


@Bot.event
async def on_message(message: discord.Message):
    # data_base.connection.commit()
    await check_lvl(message=message, vc=False)


@Bot.event
async def on_guild_join(guild: discord.Guild):
    session = db.Session()
    result = session.query(db.Config).filter_by(guild_id=guild.id).value(db.Config.guild_id)

    if result is None:
        session.add(db.Config(guild_id=guild.id))
        session.commit()

    for member in guild.members:
        if member.bot:
            continue

        user = session.query(db.Users).filter_by(user_id=member.id, guild_id=guild.id).value(db.Users.user_id)
        if user is None:
            session.add(db.Users(guild_id=guild.id, user_id=member.id, name=member.name, lvl=1, xp=0, money=0))
            session.commit()
        else:
            pass

    session.close()


@Bot.event
async def on_ready():
    session = db.Session()
    await db.create_tables()
    print(f'[!] Bot started with name {Bot.user} [ID: {Bot.user.id}]')
    for guild in Bot.guilds:
        print(f"[$] Working with {guild.id} guild.")

        for member in guild.members:
            if member.bot:
                continue

            user = session.query(db.Users).filter_by(user_id=member.id, guild_id=guild.id).value(db.Users.user_id)
            if user is None:
                session.add(db.Users(guild_id=guild.id, user_id=member.id, name=member.name, lvl=1, xp=0, money=0))
                session.commit()
            else:
                pass

        result = session.query(db.Config).filter_by(guild_id=guild.id).value(db.Config.guild_id)
        if result is None:
            session.add(db.Config(guild_id=guild.id))
            session.commit()

    database_tasks.start()
    economic_tasks.start()

    session.close()

Bot.run(token)
