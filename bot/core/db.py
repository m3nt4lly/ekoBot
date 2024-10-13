import sqlalchemy as db
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bot.cfg import database

DeclarativeBase = declarative_base()
engine = db.create_engine(f"postgresql://{database['user']}:{database['password']}@{database['host']}:{database['port']}/{database['database']}")
Session = sessionmaker(bind=engine)


class Users(DeclarativeBase):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    guild_id = db.Column(db.BigInteger)
    user_id = db.Column(db.BigInteger)
    name = db.Column(db.String)
    lvl = db.Column(db.Integer)
    xp = db.Column(db.Integer)
    money = db.Column(db.Integer)

    def __repr__(self):
        return "".format(self.code)


class Contests(DeclarativeBase):
    __tablename__ = "contests"

    message_id = db.Column(db.BigInteger, primary_key=True)
    guild_id = db.Column(db.BigInteger)
    duration = db.Column(db.DateTime)
    amount = db.Column(db.Integer)

    def __repr__(self):
        return "".format(self.code)


class Config(DeclarativeBase):
    __tablename__ = "config"

    id = db.Column(db.BigInteger, primary_key=True)
    guild_id = db.Column(db.BigInteger)
    contest_channel_id = db.Column(db.BigInteger, nullable=True)
    blacklist_channel_ids = db.Column(db.ARRAY(db.BigInteger), nullable=True)
    afk_channel_ids = db.Column(db.ARRAY(db.BigInteger), nullable=True)
    lvl5 = db.Column(db.BigInteger, nullable=True)
    lvl10 = db.Column(db.BigInteger, nullable=True)
    lvl15 = db.Column(db.BigInteger, nullable=True)
    lvl20 = db.Column(db.BigInteger, nullable=True)
    lvl20plus = db.Column(db.BigInteger, nullable=True)
    multiplier = db.Column(db.Float, nullable=True)
    xp_for_new_lvl = db.Column(db.Integer, nullable=True)
    vc_channel_notification = db.Column(db.BigInteger, nullable=True)

    def __repr__(self):
        return "".format(self.code)


async def create_tables():
    try:
        DeclarativeBase.metadata.create_all(engine)
    except exc.OperationalError:
        pass