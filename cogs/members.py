from discord.ext import commands
from cogs.utils import Checks, Utilities, FactionUpgrades
from cogs import notawiki

import discord
import random
import datetime


class Members:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def joindate(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        if member == None:
            member = ctx.author
        await ctx.send(f'{member.display_name} joined on {member.joined_at}.')

    @commands.command()
    async def resolve(self, ctx, *, member: discord.Member = None):
        """Checks how strong a member's resolve is."""
        answer = ['Vigorous!', 'Powerful!', 'Abusive!', 'Irrational!', 'Hopeless!', 'Paranoid!',
                  'Fearful!', 'Selfish!', 'Masochistic!', 'Rapturous!', 'Refracted!', 'Courageous!',
                  'Focused!', 'Stalwart!']
        if member == None:
            member = ctx.author
        embed = discord.Embed(title='{0}\'s resolve is tested...'.format(member.display_name),
                              colour=discord.Colour.dark_blue())
        embed.description = random.choice(answer)
        # await ctx.send(member.display_name + '\'s resolve is tested...')
        # await ctx.send(random.choice(answer))
        await ctx.send(embed=embed)

    @commands.command()
    async def pounce(self, ctx, member: discord.Member = None):
        """Pounce somebody with red panda pounces!"""
        if member == ctx.author:
            return await ctx.send('Aw, you can\'t pounce yourself!')

        if member == None:
            return await ctx.send('There\'s nobody to pounce :(')

        pandaImage = Utilities.getPounceImage()
        embed = discord.Embed(title=f'{ctx.author.display_name} just pounced {member.display_name}!',
                              colour=discord.Colour.red())
        embed.set_image(url='https://i.imgur.com/' + pandaImage + '.gif')
        await ctx.send(embed=embed)

    @pounce.error
    async def pounce_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send('Who are you asking me to pounce :(')

    @commands.command()
    @commands.guild_only()
    async def fact(self, ctx):
        """Cute panda facts!"""
        roll = random.randint(1, 100)
        if roll > 5:
            fact = Utilities.getpandaFact()
        else:
            fact = 'WOAH! You managed to find the elusive red panda! https://i.imgur.com/h8iQWu9.jpg'

        await ctx.send(fact)

    @commands.command()
    async def roll(self, ctx, roll: str):
        """Rolls a dice or more using #d# format."""
        resultTotal = 0
        resultString = ''

        try:
            try:
                numDice = roll.split('d')[0]
                diceVal = roll.split('d')[1]
            except Exception as e:
                print(e)
                await ctx.send(
                    f'Aw, this format looks awfully wrong! It needs to be in # d #, {ctx.author.display_name}.')
                return

            if int(numDice) > 500:
                await ctx.send('Rawr! This is too many for me \'w\' Try again! ')
                return

            async with ctx.channel.typing():
                await ctx.send(f'Rawr! Rolling {numDice}d{diceVal} for {ctx.author.display_name}!')
                rolls, limit = map(int, roll.split('d'))

                for r in range(rolls):
                    number = random.randint(1, limit)
                    resultTotal = resultTotal + number

                    if resultString == '':
                        resultString += str(number)
                    else:
                        resultString += ', ' + str(number)

                if numDice == '1':
                    await ctx.send(ctx.author.mention + ' :game_die:\n**Result:** ' + resultString)
                else:
                    await ctx.send(
                        ctx.author.mention + ':game_die:\n**Result:** ' + resultString + '\n**Total:** ' + str(
                            resultTotal))

        except Exception as e:
            print(e)
            return

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            t = ':game_die: Roll'
            desc = '**panda roll #d#**\n\nRolls a dice or more using #d#, where first # is the number on dice and ' \
                   'second # is how many rolls. '
            embed = discord.Embed(title=t, description=desc, color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @Checks.is_cookie()
    async def cookie(self, ctx):
        await ctx.send('Cookie owns this')

    @commands.command(hidden=True)
    @Checks.is_potatoe()
    async def potatoe(self, ctx):
        await ctx.send('I\'m a potato!')

    @commands.command(aliases=["upg", "u", "up"])
    @commands.guild_only()
    async def upgrade(self, ctx, arg=None, number=None):
        """Searches a Faction Upgrade from Not-a-Wiki"""
        global color
        global faction

        if arg is None and number is None:
            embed = discord.Embed(title=":recycle:  Upgrade", description="**.upgrade <faction>**\n**Aliases: **upg, "
                                                                          "up, u\n\nRetrieves a Faction upgrade "
                                                                          "information directly from Not-a-Wiki. "
                                                                          "<faction> inputs can be using two-letter "
                                                                          "Mercenary Template with upgrade number, "
                                                                          "or full Faction name with an upgrade "
                                                                          "number.\n\nExamples: Fairy 7, MK10",
                                  colour=discord.Colour.dark_gold())
            return await ctx.send(embed=embed)

        # Checking if input returns an abbreviation faction i.e. FR7 or MK11, also accepts lowercase inputs
        if arg[2].isdigit() and number is None:
            faction = arg.upper()
            argColor = faction[0:2]
            color = FactionUpgrades.getFactionColour(argColor)

        # if number is added as an input, we automatically assume the full term, i.e. "Fairy 7"
        elif number is not None:
            # Some people just like to watch the world burn
            if number < 0 or number > 12:
                raise Exception('Invalid Input')

            arg2 = arg.lower()
            arg2 = arg2.capitalize()
            checks, fac, color = FactionUpgrades.getFactionAbbr(arg2)

            # checks is retrieved from FactionUpgrades, if the term is not in dictionary it returns False and we
            # raise Exception error
            if checks is False:
                raise Exception('Invalid Input')
            else:
                faction = fac + number

        # if inputs match neither above, raise Exception
        else:
            raise Exception('Invalid Input')

        async with ctx.channel.typing():
            # We get our list through Not-a-Wiki Beautiful Soup search
            data = notawiki.factionUpgradeSearch(faction)

            # Embed things, using the list retrieved from factionUpgradeSearch
            thumbnail = data[0]
            title = f'**{data[1]}**'
            embed = discord.Embed(title=title, colour=discord.Colour(color), timestamp=datetime.datetime.utcnow())
            embed.set_footer(text="http://musicfamily.org/realm/FactionUpgrades/",
                             icon_url="http://musicfamily.org/realm/Factions/picks/RealmGrinderGameRL.png")
            embed.set_thumbnail(url=thumbnail)

            # Since the first two lines always are guaranteed to be an url and name of Faction upgrade, we ignore
            # them, and then start processing adding new fields for each line
            for line in data[2:]:
                newline = line.split(": ")
                first = f'**{newline[0]}**'
                embed.add_field(name=first, value=newline[1], inline=True)

        await ctx.send(embed=embed)

    @upgrade.error
    async def upgrade_error(self, ctx, error):
        if isinstance(error, Exception):
            title = "Error"
            embed = discord.Embed(title=title, description="Error")
            return await ctx.send(embed=embed)

    '''
    Old code for previous stuff, archiving
    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, *, role_name: str = None):
        """Adds an available role to the user"""
        newcomer = discord.utils.get(ctx.author.guild.roles, name="Newcomer")
        rolelist = [578672422862061568,
                    578672450552856591,
                    578672477497196553]

        if role_name is None:
            await ctx.send(":x: Missing role!")
            return

        print(ctx.author.roles)

        for role_id in rolelist:
            if role_id in [role.id for role in ctx.author.roles]:
                oldRole = discord.utils.get(ctx.author.guild.roles, id=role_id)
                await ctx.author.remove_roles(oldRole, newcomer)
                newRole = discord.utils.get(ctx.author.guild.roles, name=role_name)
                await ctx.author.add_roles(newRole)
                await ctx.send(f"{oldRole.name} removed and added {newRole.name}")
                return

        testRole = discord.utils.get(ctx.author.guild.roles, name=role_name)

        if testRole is None:
            await ctx.send(f":x: {testRole} doesn\'t exist!")
        else:
            await ctx.author.remove_roles(newcomer)
            await ctx.author.add_roles(testRole)
            await ctx.send(f"Added {testRole.name}!")
        
    '''


#########
def setup(bot):
    bot.add_cog(Members(bot))
