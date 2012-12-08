import simplejson
import httplib2
import urllib
import cherrypy
import urlparse
import os
from HueLight import HueLight
from ConfigurationServer import ConfigurationServer

def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/'), args))

class ConnectionException(Exception):
    pass

class Connection:
    def __init__(self, bridgeIP):
        self.bridgeIP = bridgeIP
        self.http = httplib2.Http()
        self.base_url = "http://{}".format(bridgeIP)
        self.api_key = ConfigurationServer.get('HueConnection')
        
    def authenticate(self, applicationName):
        if self.api_key == None:
            cmd = {"username": applicationName, "devicetype": applicationName}
            data = simplejson.dumps(cmd)
            resp, content = self.http.request("{}/api".format(self.base_url), method="POST",body=data)
            if resp.status != 200:
                raise ConnectionException("Returncode {} from bridge!".format(resp.status))
            cherrypy.log("{}: {}".format(resp.status, content))
            response = simplejson.loads(content)
            if 'error' in response[0].keys():
                raise ConnectionException(response[0]['error']['description'])
            self.api_key = response[0]['success']['username']
            ConfigurationServer.save('HueConnection', self.api_key)
            
            
    def send_command(self, json_cmd, api_url, request_method):
        data = simplejson.dumps(json_cmd)
        resp, content = self.http.request(urljoin(self.base_url, 'api', self.api_key, api_url), method=request_method, body=data)
        if resp.status != 200:
            raise ConnectionException("Returncode {} from bridge!".format(resp.status))
        #cherrypy.log("{}: {}".format(resp.status, content))
        response = simplejson.loads(content)
        return response

class _HueBridge:
    def __init__(self):
        self.IP = None
        self.conn = None
        self.lights = {}
        self.groups = {}
        
    def init(self, ip):
        self.IP = ip
        self.conn = Connection(self.IP)
        
    def authenticate(self):
        return self.conn.authenticate("HueControl")
        
    def update(self):
        if self.conn.api_key == None:
            return
        index_data = self.get_index()
        lights = index_data['lights']
        self.lights = {}
        for nr in lights:
            l = lights[nr]
            light = HueLight()
            light.number = int(nr)
            light.name = l['name']
            light.type = l['type']
            light.modelid = l['modelid']
            light.on = l['state']['on']
            light.bri = l['state']['bri']
            light.reachable = l['state']['reachable']
            if 'hue' in l['state']:
                light.hue = l['state']['hue']
            if 'sat' in l['state']:
                light.sat = l['state']['sat']
            if 'ct' in l['state']:
                light.ct = l['state']['ct']
            if 'xy' in l['state']:
                light.x = l['state']['xy'][0]
                light.y = l['state']['xy'][1]
            if 'colormode' in l['state']:
                light.colormode = l['state']['colormode']
            if 'sat' in l['state']:
                light.sat = l['state']['sat']
            self.lights[light.name] = light
        groups = self.get_groups()
        self.groups = { 'All Lights': 0 }
        for g in groups:
            self.groups[groups[g]['name']] = int(g)

    def set_light(self, name, param, val):
        setattr(self.lights[name], param, val)
        cmd = {param: getattr(self.lights[name], param)}
        self.conn.send_command(cmd, 'lights/{}/state'.format(self.lights[name].number), 'PUT')
    
    def get_groups(self):
        return self.conn.send_command({}, 'groups', 'GET')
        
    def set_group(self, group, param, val):
        # for now just send and update
        setattr(self.lights[self.lights.keys()[0]], param, val)
        cmd = {param: getattr(self.lights[self.lights.keys()[0]], param)}
        self.conn.send_command(cmd, 'groups/{}/action'.format(group), 'PUT')
        self.update()
        
    def get_index(self):
        return self.conn.send_command({}, '', 'GET')

HueBridge = _HueBridge()