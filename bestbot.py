
import re
import urllib, json
import urllib.request, json
import urllib.error, json
import json
import socket
import cfg.py



s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")



def chat(sock, msg):

    sock.send("PRIVMSG #{} :{}".format(cfg.CHAN, msg))


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
   if user in cfg.followsMap:
      return cfg.followsMap[user]
   else:
      try:
         r = urllib.request.urlopen("https://api.twitch.tv/kraken/users/"+user+"/follows/channels/"+CHAN+"")
         followJson = json.loads(r.read())
         if "error" in followJson:
            cfg.followsMap[user] = False
            return False
         else:
            cfg.followsMap[user] = True
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
        for pattern in cfg.PATT:
            if re.match(pattern, message):
                ban(s, username)
                break


