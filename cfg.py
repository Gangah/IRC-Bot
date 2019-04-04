host = "irc.chat.twitch.tv"              # De Database waar we info vandaan halen
port = 6667                         # De juiste port
NICK = "username"            # De naam van het account dat we gaan gebruiken
PASS = "(auth)"   # De oauth code nodig om in te loggen bij twitch
CHAN = "#gan_gah"                   # het kanaal waar onze bot aan connecteert
RATE = (20/30)                      # berichten per seconde
followsMap = {}
modsMap = {}
points: Dict[str, int] = {}

PATT = [
    r"swear",
    # ...
    r"some_pattern"
]


