import discord

from bot.core import db

economy_config_values = ['xp_for_new_lvl', 'blacklist_channel_ids', 'afk_channel_ids', 'vc_channel_notification', 'multiplier', 'lvl5', 'lvl10', 'lvl15', 'lvl20', 'lvl20plus']
contest_config_values = ['contest_channel_id']


class Config:
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.session = db.Session()

    def __exit__(self):
        self.session.close()

    def __del__(self):
        self.session.close()

    def set_value(self, config_name, value):
        self.session.query(db.Config).filter_by(guild_id=self.guild_id).update({config_name: value})
        self.session.commit()

    def get_value(self, config_name):
        data_base = self.session.query(db.Config).filter_by(guild_id=self.guild_id).first()
        if data_base:
            return getattr(data_base, config_name, None)
        return None

    def check_economy_values(self):
        config = self.session.query(db.Config).filter_by(guild_id=self.guild_id).first()
        for value in economy_config_values:
            if hasattr(config, value) and getattr(config, value) is None:
                return False
        return True

    def check_contest_values(self):
        config = self.session.query(db.Config).filter_by(guild_id=self.guild_id).first()

        if config.contest_channel_id is None:
            return False
        return True

    def create_embed(self):
        config = self.session.query(db.Config).filter_by(guild_id=self.guild_id).first()

        if any(hasattr(config, value) and getattr(config, value) is None for value in economy_config_values):
            status = "Присутствуют пустые значения"
        else:
            status = "Все значения заполнены"

        embed = discord.Embed(title="Информация о конфиге", colour=discord.Colour.from_rgb(255, 153, 0))
        embed.add_field(name="Статус", value=status, inline=False)
        for value in economy_config_values:
            if hasattr(config, value):
                embed.add_field(name=value.replace('_', ' ').title(), value=getattr(config, value), inline=True)
        embed.add_field(name="Канал для конкурсов", value=config.contest_channel_id, inline=True)

        return embed


