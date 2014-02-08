Sugar Labs IRC Help bot
=========

IRC Bot for #sugar channel
Please join to #sugar channel for test it <a href="http://chat.sugarlabs.org">Web Chat</a>

Running
-------

To run the bot you will need to first install the requirements:

    # Fedora example - run as root
    sudo yum install -y python-pip python-twisted
    pip install -e git+git://github.com/seatgeek/fuzzywuzzy.git#egg=fuzzywuzzy

Then to run the bot:

    git clone https://github.com/ignaciouy/sugar-irc
    cd sugar-irc
    python sugar-irc-bot.py
