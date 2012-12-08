import sys
sys.path.append('plugins')
sys.path.append('libs')
sys.path.append('hue')

import os
import cherrypy
import SSDP

from Scheduler import Scheduler

class HueControlStartup(object):
    def __init__(self):
        self.loaded = False
    
    def startup(self, bridge_ip):
        from Plugins import Plugins
        from HueBridge import HueBridge
        HueBridge.init(bridge_ip)
        HueBridge.update()
        self.plugins = Plugins #expose it for cherrypy
        # Automatically update every minute
        Scheduler.add_interval_job(HueBridge.update, minutes=1)

    def index(self):
        if not self.loaded:
            # find bridge and load
            resp = SSDP.discover()
            content = ''
            bridges = []
            for r in resp:
                server = resp[r].getheader('server')
                if server != None and server.find('IpBridge'):
                    bridges.append(r[0])
                    
            if len(bridges) == 1:
                # we only found one bridge, use it!
                cherrypy.log("Found bridge @ {}".format(bridges[0]))
                self.startup(bridges[0])
                self.loaded = True
                content = self.plugins.HueControl.index()
            else:
                return "More than one bridge found. We (currently) do not support multiple bridges!"
            
            return content
        else:
            return self.plugins.HueControl.index()
        
    index.exposed = True
        
global_conf = {
    'server.environment': 'development',
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8282,
}
    
cherrypy.config.update(global_conf)

app_conf = {
    '/media': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(os.getcwd(),'media'),
    },
}
cherrypy.quickstart(HueControlStartup(), config=app_conf)