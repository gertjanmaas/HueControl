import pickle
import os
import cherrypy
import glob

class _ConfigurationServer(object):
    def __init__(self):
        self.configs = {}
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        for data in glob.glob(os.path.join(self.data_dir, '*.dat')):
            data_name = os.path.splitext(os.path.basename(data))[0]
            cherrypy.log('Found configuration data for: {}'.format(data_name))
            with open(data, 'r') as config:
                self.configs[data_name] = pickle.load(config)

    def save(self, name, data):
        cherrypy.log('Saving configuration for: {}'.format(name))
        self.configs[name] = data
        filename = '{}.dat'.format(name)
        with open(os.path.join(self.data_dir, filename), 'w') as config:
                pickle.dump(self.configs[name], config)
            
    def get(self, name):
        cherrypy.log('Retrieving configuration for: {}'.format(name))
        if name in self.configs.keys():
            return self.configs[name]
        else:
            return None
            
ConfigurationServer = _ConfigurationServer()