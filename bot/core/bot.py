import discord
from discord.ext import commands


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents, command_prefix="eko.", help_command=None)

    async def setup_hook(self):
        print("[!] Bot tree syncing...")
        await self.tree.sync()