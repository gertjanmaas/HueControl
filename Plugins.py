import os
import sys
import cherrypy

class _Plugins(object):
    def __init__(self):
        plugin_dir = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'plugins')
        for plugin in os.listdir(plugin_dir):
            if plugin[0] != '.' and plugin[0] != '_':
                if os.path.isdir(os.path.join(plugin_dir, plugin)):
                    cherrypy.log("Importing plugin: {0}".format(plugin))
                    # import the module
                    m = __import__('{0}.{0}'.format(plugin), fromlist=[plugin])
                    # get the class
                    c = getattr(m, plugin)
                    # create it
                    self.__dict__[plugin] = c()
Plugins = _Plugins()