```
Ubuntu:
sudo add-apt-repository ppa:chris-lea/redis-server
sudo add-apt-repository ppa:nilya/haproxy-1.5
sudo apt-get update
sudo apt-get install libevent-dev python-software-properties redis-server haproxy
mkvirtualenv djangocon #This step is optional
pip install gevent-socketio django redis
```

Note: You’ll need MySQL or Postgres installed. I recommend using either PyMySQL or Psycopg2 as your database connector. I think these are also the standard python libraries for their respective database.

It’s also likely that part of gevent-socketio won’t get installed (I think there’s something wrong with the pip package). For some reason the sdjango.py module never seems to copy over for me. cd to your python packages folder and put sdjango.py in your socketio folder. This is how I did it.

```
cd ~/.virtualenvs/djangocon/lib/python2.7/site-packages/socketio/
wget https://raw.github.com/abourget/gevent-socketio/master/socketio/sdjango.py
```

```
//Node.js (optional stuff)
npm install -g websocket-bench
```

If you run in to any issues please let me know and I'll try and help the best I can. I've tested all this code on Ubuntu 13.04 running inside of a virtualbox.