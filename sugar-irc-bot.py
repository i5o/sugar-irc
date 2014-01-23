#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    IRC Bot for help users in #sugar channels (Freenode)
#    Copyright (C) 2014, Ignacio Rodríguez <ignacio@sugarlabs.org>
#                        Sam Parkinson     <sam.parkinson3@gmail.com>
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

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

from msg_scan import scan_msg, they_know_now, they_dont_know

HELP_TXT = ": Hi! Why don't you check out this: " + \
        "https://github.com/ignaciouy/sugar-irc/wiki/Resources-for-New-Devs"
BOT_INFO_TXT = ": Hi! I'm a bot by Ignacio and SAMdroid that's here to help. "+\
        "You can find my code here: https://github.com/ignaciouy/sugar-irc"
BOT_HELP_TXT = ": Help is on my wiki: " + \
        "https://github.com/ignaciouy/sugar-irc/wiki/SugarBot-Help"

class SugarIRCBOT(irc.IRCClient):
    nickname = "sugarbot"
    realname = "Sugar Labs help bot"

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        self.join("sugar")

    def joined(self, channel):
        pass

    def privmsg(self, user, channel, msg):
        addressed = False
        if msg.startswith(self.nickname):
            msg = msg[len(self.nickname)+1:]
            addressed = True
        msg.strip()
        msg = msg.lower()

        nice_user = user.split('!')[0]

        if scan_msg(msg, nice_user):
            self.msg(channel, nice_user+HELP_TXT)

        if ('i know' in msg or 'no spam for me' in msg) and addressed:
            they_know_now(nice_user)
            self.msg(channel, 'I now count %s as smart' % nice_user)
            return

        if 'spam me' in msg and addressed:
            they_dont_know(nice_user)
            self.msg(channel, nice_user+": you will now be help spammed")
            return

        if 'help' in msg and addressed:
            self.msg(channel, nice_user+BOT_HELP_TXT)
            return

        if 'info' in msg and addressed:
            self.msg(channel, nice_user+BOT_INFO_TXT)
            return

        if 'ping' in msg and addressed:
           self.msg(channel, nice_user+': PONG')
           return

        if 'freetime' in msg and addressed:
            self.msg(channel, "gcibot, I love you. We should go out some time")

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
    reactor.connectTCP("irc.freenode.net", 6667, f)
    reactor.run()
