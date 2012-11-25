import mako.template
import Template
from xml.etree import ElementTree
import datetime
import time
import httplib2
import urllib2
import cherrypy
import random
import simplejson

from HueBridge import HueBridge
from Scheduler import Scheduler
from ConfigurationServer import ConfigurationServer

EARTHTOOLS_URL = 'http://www.earthtools.org/sun/' #<lat>/<long>/<day>/<month>/<timezone>/<dst>

class AutoOn(object):
    def __init__(self):
        self.http = httplib2.Http()
        self.config = ConfigurationServer.get('AutoOn')
        if self.config == None:
            self.config = {
                'lat': 0,
                'long': 0,
                'city': 'Enter a city here...',
                'offset': 0,
            }
        minute = random.randint(0,59)
        start_date = datetime.datetime.combine(datetime.datetime.today(), datetime.time(hour=12, minute=minute, second=0)) #added randomness to not break earthtools :)
        if start_date < datetime.datetime.now():
            # get the sunset for today, the get_sunset function will take care of the rest
            self.get_sunset()
            start_date += datetime.timedelta(days=1)
        Scheduler.add_interval_job(self.get_sunset, days=1, start_date=start_date)
        
        
    def get_sunset(self):
        # 0,0 is a gps coordinate somewhere in the South Atlantic Ocean, hopefully nobody uses Hue there :)
        if self.config['lat'] != 0 and self.config['long'] != 0:
            now = datetime.datetime.now()
            request_url = "{}/{}/{}/{}/{}/99/1".format(EARTHTOOLS_URL, self.config['lat'], self.config['long'], now.day, now.month)
            resp, content = self.http.request(request_url, method="GET")
            if int(resp['status']) == 200:
                xml = ElementTree.fromstring(content)
                sunset = xml.find(".//evening/sunset")
                sunset_time = time.strptime(sunset.text, "%H:%M:%S")
                sunset_datetime = datetime.datetime(now.year, now.month, now.day, sunset_time.tm_hour, sunset_time.tm_min, sunset_time.tm_sec) + datetime.timedelta(minutes=self.config['offset'])
                if sunset_datetime > datetime.datetime.now():
                    cherrypy.log("AutoOn: Turning lights on @ {}".format(sunset_datetime))
                    Scheduler.add_date_job(self.turn_lights_on, sunset_datetime)
    
    def turn_lights_on(self):
        HueBridge.set_group(0, 'on', 'true')
    
    def save(self, **jsonData):
        loc = jsonData['location']
        offset = int(jsonData['offset'])
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=false".format(urllib2.quote(loc))
        req = urllib2.urlopen(geocode_url)
        resp = simplejson.loads(req.read())
        self.config['lat'] = resp['results'][0]['geometry']['location']['lat']
        self.config['long'] = resp['results'][0]['geometry']['location']['lng']
        self.config['city'] = loc
        self.config['offset'] = offset
        ConfigurationServer.save('AutoOn', self.config)
    
    def index(self):
        template = mako.template.Template(filename='plugins/AutoOn/AutoOn.tmpl')
        rendered_template = template.render(config=self.config)
        return Template.render_template(rendered_template)
    
    save.exposed = True
    index.exposed = True