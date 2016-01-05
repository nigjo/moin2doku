from MoinMoin.server.standalone import StandaloneConfig, run

import sys
# Path of the directory where wikiconfig.py is located.
# YOU NEED TO CHANGE THIS TO MATCH YOUR SETUP.
sys.path.insert(0, 'home/caddy/wikifarm/var/wikifarm/config')

# Path to MoinMoin package, needed if you installed with --prefix=PREFIX
# or if you did not use setup.py.
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages')

# Path of the directory where farmconfig.py is located (if different).
sys.path.insert(0, '/home/caddy/wikifarm/var/wikifarm/config')

class Config(StandaloneConfig):
    docs = '/home/caddy/wikifarm/var/wikifarm'
    user = 'http'
    group = 'http'
    port = 80
            
run(Config)
        