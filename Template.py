import mako.template
from mako.lookup import TemplateLookup
from HueBridge import HueBridge

def render_template(plugin_content, error=""):
    # importing plugins here, else there's a circular dependency :(
    from Plugins import Plugins
    lookup = TemplateLookup(directories=['.'])
    template = mako.template.Template(filename='templates/index.tmpl', lookup=lookup)
    return template.render(BRIDGE_IP=HueBridge.IP, PLUGIN_CONTENT=plugin_content, plugins=Plugins.__dict__.keys(), error=error)