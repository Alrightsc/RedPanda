from discord.ext import commands
from cogs.utils import Checks, Utilities, FactionUpgrades
from bs4 import BeautifulSoup
from urlextract import URLExtract

import datetime
import discord
import requests

badSubstrings = ["", "Cost", "Effect", "Formula", "Mercenary Template", "Requirement", "Gem Grinder and Dragon's "
                                                                                       "Breath Formula"]

def format(lst: list, factionUpgrade):
    """Formats the list retrieved from BeautifulSoup"""

    # First line always return an url - we want to get the URL only for the thumbnail
    url = lst[0]
    extractor = URLExtract()
    newUrl = extractor.find_urls(url)

    # We remove the line from list and replace with the new url
    lst.remove(url)
    lst.insert(0, newUrl[0])

    # We add the faction upgrade name to the list so embed can refer to this
    lst.insert(1, factionUpgrade)

    # For 10-12 upgrades, we want Cost to be first after Requirement, to look nice in Embed
    if lst[3].startswith('Requirement'):
        old = lst[3]
        new = lst[4]
        lst[3] = new
        lst[4] = old

    # Cleanup in case bad stuff goes through somehow
    for line in lst[3:]:
        if line in badSubstrings:
            lst.remove(line)

        # Notes are not really important for the embed
        if line.startswith("Note"):
            lst.remove(line)

    # A little extra for Djinn 8 - show current UTC time and odd/even day
    if factionUpgrade == "Flashy Storm":
        utc_dt = datetime.datetime.utcnow()
        day = int(utc_dt.strftime("%d"))
        dj8 = ""
        if day % 2 == 0:
            dj8 = ", Odd-tier Day"
        elif day % 2 == 1:
            dj8 = ", Even-tier Day"

        lst.append(f'Current Time (UTC): {utc_dt.strftime("%H:%M")}' + dj8)

    return lst


def factionUpgradeSearch(faction):
    # Getting the Upgrade from FactionUpgrades
    factionUpgrade = FactionUpgrades.getFactionUpgradeName(faction)

    # Retrieving data using Request and converting to BeautifulSoup object
    nawLink = "http://musicfamily.org/realm/FactionUpgrades/"
    content = requests.get(nawLink)
    soup = BeautifulSoup(content.content, 'html5lib')

    # Searching tags starting with <p>, which upgrades' lines on NaW begin with
    p = soup.find_all('p')

    # Our upgrade info will be added here
    screen = []

    # Iterating through p, finding until upgrade matches
    for tag in p:
        # space is necessary because there is always one after image
        if tag.get_text() == " " + factionUpgrade:
            # if True, adds full line so we can retrieve the image through our formatting function
            screen.append(str(tag))

            # Since we return true, we search using find_all_next function, and then break it there since we don't
            # need to iterate anymore at the end
            for line in tag.find_all_next(['p','br','hr','div']):
                # Not-a-Wiki stops lines after a break, a new line, or div, so we know the upgrade info stop there
                if str(line) == "<br/>" or str(line) == "<hr/>" or str(line).startswith("<div"):
                    break
                else:
                    # Otherwise, add the lines of upgrade to the list - line.text returns the text without HTML tags
                    screen.append(line.text)
            break

    # Then we run the list through a formatter, and that becomes our new list
    return format(screen, factionUpgrade)