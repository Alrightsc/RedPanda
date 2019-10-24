from discord.ext import commands
from cogs.utils import Checks, Utilities, FactionUpgrades
from bs4 import BeautifulSoup, NavigableString
from urlextract import URLExtract

import discord
import requests

badSubstrings = ["", "Cost", "Effect", "Formula", "Mercenary Template", "Requirement"]

def format(list: list):
    """Formats the list retrieved from BeautifulSoup"""

    url = list[0]
    extractor = URLExtract()
    newUrl = extractor.find_urls(url)
    list.remove(url)
    list.insert(0, newUrl[0])
    list[1] = list[1].strip()

    for x in range(len(list)):
        for line in list[1:x]:
            if line in badSubstrings:
                list.remove(line)

            if line.startswith("Note"):
                list.remove(line)

    return list

def factionUpgradeSearch(faction):
    #Getting the Upgrade
    factionUpgrade = FactionUpgrades.getFactionUpgradeName(faction)
    nawLink = "http://musicfamily.org/realm/FactionUpgrades/"
    content = requests.get(nawLink)
    soup = BeautifulSoup(content.content, 'html5lib')

    p = soup.find_all('p')
    screen = []
    for tag in p:
        if tag.get_text() == " " + factionUpgrade:
            screen.append(str(tag))
            for line in tag.find_all_next():
                if str(line) == "<br/>" or str(line) == "<hr/>" or str(line) == "</div>":
                    break
                else:
                    screen.append(line.text)
            break

    screen = format(screen)
    return screen


print(factionUpgradeSearch("EL10"))