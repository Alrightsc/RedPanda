import random

pandaPounceImgLst = ['ZryMhjR',
          'JeoFUtc',
          '6sBwuC9',
          'u8JsVe7',
          'gWEzfh4']

def getPounceImage():
    return random.choice(pandaPounceImgLst)

pandaFacts = [
            'Rawr! Red pandas are crepuscular, meaning they are active during twilight hours (dusk and dawn). They can be usually seen sleeping during the days and become more active in the evenings.',
            'Awww! Although small for their size, red pandas stand on their legs to appear bigger when threatened.',
            'Yum! Commonly red pandas are seen eating bamboo, but they actually eat many more varieties, such as small mammals, eggs, flowers, berries, and even were observed to eat birds, maple, leaves, and barks of certain trees in captivity.',
            'Noo! Red pandas are currently considered endangered as per the ICUN Red List since 2008 due to many factors, which are usually human-related (hunting and deforestation of the wild leading to habitat loss/fragmentation). In wild, there are as many 2,500 to 16,000-20,000 red pandas worldwide.',
            'Copy-panda? Red pandas are actually not the giant pandas\' relative - they are more closely associated to skunks, raccoons, otters and the like rather than actual bears or the giant panda.',
            'Awooo! Did you know you can donate to help the red pandas? You can be a member at https://www.redpandanetwork.org/ where they do efforts on helping reduce deforestation, encourage eco-trips, and raise awareness about the beautiful animals. You also get a t-shirt!',
            'Rawr I\'m THE PANDA! Although the panda tends to be commonly correlated to the black-and-white bears, red pandas were actually discovered first! A French zoologist, Frédéric Cuvier, was the first to describe the western red panda Ailurus fulgens in 1825, 48 years before the giant panda was catalogued.',
            'I\'M A CUTE PANDA. Although red pandas are notoriously adorable, the coloring marks on their face/fur are intentional! The red/white tears extending from the eyes appear luminescent to help the mother guide her cubs in the darkness. Their red fur meshes very well with the mosses growing on trees where they often hide, and the black on their stomach makes it difficult to see them from below.',
            'GIVE ME THE BAMBOO! The word panda comes from Nepalese language, nigalya poonya, translated literally meaning "eater of bamboo", or bamboo footed. Additionally, their scientific name Ailurus fulgens literally means fire cat. They are also referred as fire foxes, red cats, fox bears, bright pandas, and sometimes Himalayan raccoon.']

def getpandaFact():
    return random.choice(pandaFacts)