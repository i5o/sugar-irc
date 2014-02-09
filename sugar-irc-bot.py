#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    IRC Bot for help users in #sugar channels (Freenode)
#    Copyright (C) 2014, Ignacio Rodríguez <ignacio@sugarlabs.org>
#    Copyright (C) 2014, Sam Parkinson     <sam.parkinson3@gmail.com>
#    Copyright (C) 2014, Sai Vineet        <saivineet89@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import getpass
import signal
import sys
import re

from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

from msg_scan import scan_msg, they_know_now, they_dont_know

AUTHORS = "Sam Parkinson, Sai Vineet, and Ignacio Rodriguez"

HELP_TXT = ("Hi! Why don't you check out this: "
            "http://developer.sugarlabs.org/what-can-i-do.md.html")

BOT_INFO_TXT = ("Hi! I'm a bot by {authors} that's here to help. "
                "You can find my code here: "
                "https://github.com/ignaciouy/sugar-irc")
BOT_INFO_TXT = BOT_INFO_TXT.format(authors=AUTHORS)

BOT_HELP_TXT = (": Help is on my wiki: "
                "https://github.com/ignaciouy/sugar-irc/wiki/SugarBot-Help")

BOT_VERSION = "7:51 PM, Friday, February 7, 2014 (UTC)"

UPDATE_RE = ("\[sugar-irc\] [a-zA-Z0-9-`]{1,999} pushed "
             "[0-9]{1,999} new commit[s]{0,1} to master: http://git.io/.*")

# The sugar channel bots, or ignored. Dont talk with him.
IGNORED_BOTS = ["meeting", "soakbot", "gcibot", "github",
                "sbbot", "sugarbot-git"]


class SugarIRCBOT(irc.IRCClient):
    nickname = "sugarbot"
    realname = "Sugar Labs help bot"
    username = "sugarbot"
    # Ask password (for sugarbot account) to Ignacio or Sam
    # If password already exists: this use the first typed password.
    # Btw: You can use: python sugar-irc-bot.py password
    if len(sys.argv) == 1:
        password = getpass.getpass("irc password: ")
    else:
        password = sys.argv[1]

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        self.join("sugar")

    def joined(self, channel):
        self.msg(channel, BOT_INFO_TXT)

    def privmsg(self, user, channel, msg):
        addressed = False

        if msg.startswith(self.nickname):
            msg = msg[len(self.nickname)+1:]
            addressed = True

        msg.strip()
        msg = msg.lower()

        nice_user = user.split('!')[0]

        # Restart the bot if the user is sugarbot-git
        # We need to find a elegant way.
        if "sugarbot-git" in nice_user and re.match(UPDATE_RE, msg):
            self.msg(channel, 'I will update now')
            reactor.stop()

        for ignored in IGNORED_BOTS:
            if ignored in nice_user.lower():
                # Just talking with bot :(
                return

        if scan_msg(msg, nice_user):
            self.msg(channel, nice_user + ', ' + HELP_TXT)

        if ('i know' in msg or 'no spam for me' in msg) and addressed:
            they_know_now(nice_user)
            self.msg(channel, 'I now count %s as smart' % nice_user)
            return

        msg_match = ('spam me' in msg or 'i don\'t know' in msg or
                     'i dont know' in msg)
        if msg_match and addressed:
            they_dont_know(nice_user)
            self.msg(channel, nice_user + ", you will now be help spammed")
            return

        re_result = re.search("([\S]{1,9999}) knows", msg)
        if re_result and addressed:
            they_know_now(re_result.groups()[0])
            self.msg(channel, 'I now count %s as smart' %
                     re_result.groups()[0])
            return

        if 'help' in msg and addressed:
            self.msg(channel, nice_user + BOT_HELP_TXT)
            return

        if ('info' in msg or 'hi' in msg) and addressed:
            self.msg(channel, nice_user + ", " + BOT_INFO_TXT)
            return

        if 'ping' in msg and addressed:
            self.msg(channel, nice_user + ', pong')
            return

        if 'version' in msg and addressed:
            self.msg(channel, nice_user + ': ' + BOT_VERSION)
            return

        if 'freetime' in msg and addressed:
            self.msg(channel, "gcibot, I love you. We should go out some time")
            return


class BotFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        p = SugarIRCBOT()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()


if __name__ == '__main__':
    f = BotFactory()
    reactor.connectTCP("rajaniemi.freenode.net", 6667, f)
    reactor.run()
