from discord.ext import commands
from cogs.utils import Checks, Utilities, FactionUpgrades
from bs4 import BeautifulSoup, NavigableString
from urlextract import URLExtract

import discord
import requests

badSubstrings = ["", "Cost", "Effect", "Formula", "Mercenary Template", "Requirement"]

def format(list: list):
    """Formats the list retrieved from BeautifulSoup"""

    # First line always return an url - we want to get the URL only for the thumbnail
    url = list[0]
    extractor = URLExtract()
    newUrl = extractor.find_urls(url)

    # We remove the line from list and replace with the new url
    list.remove(url)
    list.insert(0, newUrl[0])

    # Not-a-Wiki always begin with a space in the upgrade name, so we strip it
    list[1] = list[1].strip()

    # Since BeautifulSoup returns each line per tag <>, we just get rid of these using the badSubstrings above
    for x in range(len(list)):
        for line in list[1:x]:
            if line in badSubstrings:
                list.remove(line)

            if line.startswith("Note"):
                list.remove(line)

    return list


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
            for line in tag.find_all_next():
                # Not-a-Wiki stops lines after a break, a new line, or div, so we know the upgrade info stop there
                if str(line) == "<br/>" or str(line) == "<hr/>" or str(line) == "</div>":
                    break
                else:
                    # Otherwise, add the lines of upgrade to the list - line.text returns the text without HTML tags
                    screen.append(line.text)
            break

    # Then we run the list through a formatter, and that becomes our new list
    return format(screen)


print(factionUpgradeSearch("EL10"))
