
import re
import urllib, json
import urllib.request, json
import urllib.error, json
import json
import socket
from typing import Dict


host = "irc.chat.twitch.tv"              # De Database waar we info vandaan halen
port = 6667                         # De juiste port
NICK = "InformaticaBot"            # De naam van het account dat we gaan gebruiken
PASS = "oauth:hb8wg07zchgu1wkdzpmxoqk038196g"   # De oauth code nodig om in te loggen bij twitch
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

s = socket.socket()
s.connect((host,port))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")



def chat(sock, msg):

    sock.send("PRIVMSG #{} :{}".format(CHAN, msg))


def ban(sock, user):

    chat(sock, ".ban {}".format(user))


def timeout(sock, user, secs=600):

    chat(sock, ".timeout {}".format(user, secs))

def getUser(line):
   user = ""
   if line[1] == "PRIVMSG":
      user = line[0]
      user = user.split("!")
      user = user[0]
      user = user[1:]
   return user
def getMessage(line):
   line = line[3:]
   line = ' '.join(line)
   return line[1:].split(' ')
def follows(user):
   global CHANNEL_NAME
   if user in followsMap:
      return followsMap[user]
   else:
      try:
         r = urllib.request.urlopen("https://api.twitch.tv/kraken/users/"+user+"/follows/channels/"+CHAN+"")
         followJson = json.loads(r.read())
         if "error" in followJson:
            followsMap[user] = False
            return False
         else:
            followsMap[user] = True
            return True
      except:
         return False





while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r'\w+', response).group(0)  # return the entire match
        message = CHAT_MSG.sub("", response)
        print(username + ": " + message)
        for pattern in PATT:
            if re.match(pattern, message):
                ban(s, username)
                break


