```
Ubuntu:
sudo add-apt-repository ppa:chris-lea/redis-server
sudo add-apt-repository ppa:nilya/haproxy-1.5
sudo apt-get update
sudo apt-get install libevent-dev python-software-properties redis-server haproxy python-dev
mkvirtualenv djangocon #This step is optional
pip install gevent-socketio django redis
```

Note: You’ll need MySQL or Postgres installed. I recommend using either PyMySQL or Psycopg2 as your database connector. I think these are also the standard python libraries for their respective database.

It’s also likely that part of gevent-socketio won’t get installed (I think there’s something wrong with the pip package). For some reason the sdjango.py module never seems to copy over for me. cd to your python packages folder and put sdjango.py in your socketio folder. This is how I did it.

```
cd ~/.virtualenvs/djangocon/lib/python2.7/site-packages/socketio/
wget https://raw.github.com/abourget/gevent-socketio/master/socketio/sdjango.py
```

You'll also probably need to edit the default haproxy file.

```
sudo nano /etc/default/haproxy
ENABLED=1
```


```
//Node.js (optional stuff)
npm install -g websocket-bench
```

If you run in to any issues please let me know and I'll try and help the best I can. I've tested all this code on Ubuntu 13.04 running inside of a virtualbox.

## Running Haproxy with SSL + Socket.io

This is the article I mentioned during my talk that I found super useful. [Check it out](http://blog.carbonfive.com/2013/05/02/using-haproxy-with-socket-io-and-ssl/) 

## How To Run Fantasy

The fantasy project is a mostly complete project though there are a few areas for improvement. The goal of fantasy is to allow you to create a league. Then 4 teams can signup for that league. Once 4 teams have signed up for that league the draft will start. You can pick two people from the list of players and everyones team at the bottom will automatically be updated. The draft works like a standard snake draft in fantasy football.

This example also includes how to use the built-in ACL and error functions for the gevent-socketio project. If it's not your pick you don't have access to the pick event.

1. Run python manage.py syncdb. When asked to create a superuser you can say no if you want. There are fixtures for this project which will create users and plays for us.
2. There are 4 users by default (max, max1, max2, max3). The password for each user is max
3. Start the server with python manage.py rs
4. Open 4 new browser sessions. I used firefox, firefox private window, chrome, and chrome private window. Then login with each of the users listed in step 2.
5. In one of the windows go ahead and input a league name and press enter. This will then open up a league for people to signup for.
6. For each window type in a team name under the league you just created. When you press enter you will be taken to the draft room.
7. When 4 people have joined the draft the current pick will be set (Draft order is randomized at start).
8. In the window of the current pick go ahead and click on a player. The team rosters at the very bottom of the page should be updated instantly. The player will also be removed from the pool of draftable players.
9. You can test that the ACL is working by attempting to draft a player with a team who isn't set as the current pick.
10. After everyone has draft 2 players the draft will end.

I went through and made sure to add extra detailed comments for sockets.py. If you have any further questions about this project or any of the others please feel free to open up an issue or contact me through my website.

---

If you make any improvements on any of code please submit a pull request. Also feel free to add example projects of your own. I'll also be here at Djangocon through Saturday (Sept. 7th).

All code in this repo is provided under the MIT license so feel free to do with it as you please.