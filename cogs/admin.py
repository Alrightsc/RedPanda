import datetime
from collections import Counter

import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def purge(self, ctx, limit: int, *, before=None, after=None):
        if limit > 2000:
            return await ctx.send('Rawr! This is too many apples! Please try giving me smaller slices :( (2000 messages maximum)')

        if before is None:
            before = ctx.message
        else:
            before = discord.Object(id=before)

        if after is not None:
            after = discord.Object(id=after)

        try:
            deleted = await ctx.channel.purge(limit=limit, before=before, after=after)
        except discord.Forbidden:
            return
        except discord.HTTPException:
            return await ctx.send('Rawr! This is too many apples! Please try giving me smaller slices :( (2000 messages maximum)')

        spammers = Counter(m.author.display_name for m in deleted)
        deleted = len(deleted)
        messages = [f'Pouncing time! {deleted} message{" was" if deleted == 1 else "s were"} removed.']
        if deleted:
            messages.append('')
            spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
            messages.extend(f'**{name}**: {count}' for name, count in spammers)

        to_send = '\n'.join(messages)

        if len(to_send) > 2000:
            await ctx.send(f'Successfully pounced {deleted} messages!', delete_after=30)
        else:
            await ctx.send(to_send, delete_after=30)

        desc = f'**Purged {deleted} messages in {ctx.channel.mention}!**'
        time = datetime.datetime.utcnow()
        fmt = '%h'
        e = discord.Embed(description=desc, colour=discord.Colour.red())
        e.set_author(name=ctx.author.mention, icon_url=ctx.author.avatar_url)
        e.set_footer(text=datetime.datetime.utcnow())
        target = discord.utils.get(ctx.message.guild.channels, name="mod-logs")
        await target.send(embed=e)
###
def setup(bot):
    bot.add_cog(Admin(bot))