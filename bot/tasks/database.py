from bot.core import Bot, db


async def update():
    session = db.Session()
    for guild in Bot.guilds:
        print(f"[$] Updating database values... guild - {guild.id}")
        for member in guild.members:
            if member.bot:
                continue
            data_base = session.query(db.Users).filter(db.Users.user_id == member.id, db.Users.guild_id == guild.id).first()
            db_name = data_base.name
            discord_name = member.name
            if db_name != discord_name:
                try:
                    session.query(db.Users).filter(db.Users.user_id == member.id, db.Users.guild_id == guild.id).update({db.Users.name: discord_name})
                except Exception as exception:
                    print("[!] Updating with errors. Some users not in server.")
                    print(f"[*] Error log: {exception}")
        session.commit()
    session.close()
