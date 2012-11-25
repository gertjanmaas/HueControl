import sys
sys.path.append('plugins')
sys.path.append('libs')
sys.path.append('hue')

import os
import cherrypy
from Plugins import Plugins
from HueBridge import HueBridge
from Scheduler import Scheduler

class HueControlStartup(object):
    def __init__(self):
        HueBridge.update()
        self.plugins = Plugins #expose it for cherrypy
        # Automatically update every minute
        Scheduler.add_interval_job(HueBridge.update, minutes=1)

    def index(self):
        return Plugins.HueControl.index()
        
    index.exposed = True
        
global_conf = {
    'server.environment': 'development',
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
}
    
cherrypy.config.update(global_conf)

app_conf = {
    '/media': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(os.getcwd(),'media'),
    },
}
cherrypy.quickstart(HueControlStartup(), config=app_conf)