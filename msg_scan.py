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

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

they_know = []
if os.path.isfile('they_know.txt'):
    with open('they_know.txt') as f:
        they_know = f.read().split(',')

help_signs = [
    ("i'm", 'new'),
    ('i', ('want', 'would'), 'to', ('help', 'contribute'))
]

MIN_SCORE = 0.8

def get_help_sign_score(msg, sign):
    """
    Returns how sure the bot is that a the given sign is in the msg
    Returns between 0 and 1
    """
    score = 0
    for word in sign:
        if isinstance(word, str):
            if word in msg:
                score += 1
        else:
            for x in word:
                if x in msg:
                    score += 1
                    break
    return float(score)/len(sign)

def scan_msg(msg, user):
    """
    Scan the message to see if the person needs help
    """
    if user.lower() in they_know:
        return False

    for i in help_signs:
        if get_help_sign_score(msg, i) > MIN_SCORE:
            return True
