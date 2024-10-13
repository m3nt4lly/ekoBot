from bot.config.cfg_manager import Config
from bot.core import db
from bot.core import Bot
import discord


async def give_role(member: discord.Member):
    cfg = Config(member.guild.id)
    session = db.Session()
    lvl = session.query(db.Users.lvl).filter_by(user_id=member.id, guild_id=member.guild.id).scalar()
    lvl5 = member.guild.get_role(cfg.get_value('lvl5'))
    lvl10 = member.guild.get_role(cfg.get_value('lvl10'))
    lvl15 = member.guild.get_role(cfg.get_value('lvl15'))
    lvl20 = member.guild.get_role(cfg.get_value('lvl20'))
    lvl20plus = member.guild.get_role(cfg.get_value('lvl20plus'))

    if lvl is None:
        session.add(db.Users(user_id=member.id, guild_id=member.guild.id, name=member.name, lvl=1, xp=0, money=0))
        session.commit()
        lvl = 1

    if int(lvl) >= 5:
        await member.add_roles(lvl5)
    if int(lvl) >= 10:
        await member.remove_roles(lvl5)
        await member.add_roles(lvl10)
    if int(lvl) >= 15:
        await member.remove_roles(lvl10)
        await member.add_roles(lvl15)
    if int(lvl) == 20:
        await member.remove_roles(lvl15)
        await member.add_roles(lvl20)
    if int(lvl) >= 21:
        await member.remove_roles(lvl20)
        await member.add_roles(lvl20plus)

    session.close()


async def check_lvl(vc: bool = None, message: discord.Message = None):
    session = db.Session()
    if vc:
        for guild in Bot.guilds:
            config = Config(guild.id)
            if not config.check_economy_values():
                continue

            afk_channel_ids = config.get_value('afk_channel_ids')
            for member in guild.members:
                if member.bot:
                    continue

                if member.voice and member.voice.channel and member.voice.channel.id not in afk_channel_ids:
                    user = session.query(db.Users).filter_by(user_id=member.id, guild_id=guild.id).first()
                    if user:
                        current_xp = user.xp
                        current_lvl = user.lvl
                        current_xp += 1

                        xp_for_new_lvl = config.get_value('xp_for_new_lvl')
                        multiplier = config.get_value('multiplier')
                        if current_xp >= (xp_for_new_lvl * current_lvl) ** multiplier:
                            channel = Bot.get_channel(config.get_value('vc_channel_notification'))
                            current_lvl += 1
                            current_xp = 0
                            embed = discord.Embed(description=f"{member.mention}, теперь у тебя {current_lvl} уровень!",
                                                  colour=discord.Colour.from_rgb(68, 148, 74))
                            await channel.send(embed=embed)
                            user.lvl = current_lvl
                            await give_role(member=member)

                        user.xp = current_xp
                        session.commit()
    else:
        if message.author.bot:
            return

        config = Config(message.guild.id)
        if not config.check_economy_values():
            return

        blacklist_channels_ids = config.get_value('blacklist_channel_ids')
        if message.channel.id in blacklist_channels_ids:
            return

        user = session.query(db.Users).filter_by(user_id=message.author.id, guild_id=message.guild.id).first()
        if user:
            current_xp = user.xp
            current_lvl = user.lvl
            current_xp += 1

            xp_for_new_lvl = config.get_value('xp_for_new_lvl')
            multiplier = config.get_value('multiplier')
            if current_xp >= (xp_for_new_lvl * current_lvl) ** multiplier:
                current_lvl += 1
                current_xp = 0
                embed = discord.Embed(description=f"{message.author.mention}, теперь у тебя {current_lvl} уровень!",
                                      colour=discord.Colour.from_rgb(68, 148, 74))
                await message.channel.send(embed=embed)
                user.lvl = current_lvl
                await give_role(member=message.author)

            user.xp = current_xp
            session.commit()

    session.close()
