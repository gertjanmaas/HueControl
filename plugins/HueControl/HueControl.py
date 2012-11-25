import mako.template
from mako.lookup import TemplateLookup
from HueBridge import HueBridge, ConnectionException
import Template
import colorsys
import os
import sys
import cherrypy

class HueControl(object):        
    def index(self):
        # for debug purposes:
        #HueBridge.update()
        template = mako.template.Template(filename='plugins/HueControl/HueControl.tmpl')
        try:
            # Check the authentication with the bridge
            HueBridge.authenticate()
            HueBridge.update()
        except ConnectionException as e:
            return Template.render_template("", error="Bridge is not authenticated! Press the link button and <a href=\"\"> try again</a>!")
            
        rendered_template = template.render(lights=HueBridge.lights, groups=HueBridge.groups)
        return Template.render_template(rendered_template)
        
    def control_light(self, light_name, param, val):
        HueBridge.set_light(light_name, param, val)
    
    def control_group(self, group_name, param, val):
        group_nr = HueBridge.groups[group_name]
        HueBridge.set_group(group_nr, param, val)
        
    control_light.exposed = True
    control_group.exposed = True
    index.exposed = True