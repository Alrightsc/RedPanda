from discord.ext import commands
from cogs.config import get_token

import discord
import datetime
import sys
import traceback


description = 'Rawr! I\'m a Red Panda bot written by Alright#2304.\nUse either "panda" as a prefix, or ping the bot ' \
              'to use the commands below.\n\nFeel free to suggest any extra commands to give this bot some more love! '

extensions = ['cogs.members',
              'cogs.admin',
              'cogs.owner']

def getPrefix(bot, msg):
    prefixes = ['panda ', 'Panda ']
    return commands.when_mentioned_or(*prefixes)(bot, msg)

class RedPanda(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=getPrefix, description=description, help_attrs=dict(hidden=True))

        for extension in extensions:
            try:
                self.load_extension(extension)
            except Exception:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        await self.change_presence(status=discord.Status.online, activity=discord.Game('I\'m a red panda!'))

        print(f'Ready to pounce! {self.user} (ID: {self.user.id})')

    """
    archived code
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name="Newcomer")
        await member.add_roles(role)
    """

    def run(self):
        super().run(get_token(), reconnect=True)


if __name__ == '__main__':
    bot = RedPanda()
    bot.run()