#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    IRC Bot for help users in #sugar channels (Freenode)
#    Copyright (C) 2014, Sam Parkinson <sam.parkinson3@gmail.com>
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
import json

from fuzzywuzzy import fuzz

data = {'they_know': []}
if os.path.isfile('data.json'):
    with open('data.json') as f:
        data = json.load(f)

brain = {'langs': []}
if os.path.isfile('brain.json'):
    with open('brain.json') as f:
        brain = json.load(f)

MIN_SCORE = 95  # Out of 100
sent_count = {}

SPAM_HELP_TEXT = ("Am I spaming you? If so please type "
                  " 'sugarbot: i know' and I won't spam you")

def scan_msg(msg, user):
    """
    Scan the message to see if the person needs help
    """
    if sent_count.get(user, 0) == 1:
        return SPAM_HELP_TEXT

    if user.lower() in data['they_know']:
        return False

    for lang in brain['langs']:
        for i in lang['signs']:
            if fuzz.partial_ratio(str(i), msg) > MIN_SCORE:
                sent_count[user] = sent_count.get(user, 0) + 1
                return str(lang['out'])


def _save_data():
    with open('data.json', 'w') as f:
        json.dump(data, f)


def they_know_now(nick):
    global data
    nick = nick.lower()
    if not nick in data['they_know']:
        data['they_know'].append(nick)
        _save_data()


def they_dont_know(nick):
    global data
    nick = nick.lower()
    if nick in data['they_know']:
        data['they_know'].remove(nick)
        _save_data()
