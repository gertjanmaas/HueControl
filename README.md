HueControl
==========

*Just a heads up: This is my first open source project, first use of most of the python plugins 
and first time use of git (and github), so bear with me. :)*

HueControl is a python application to control your Philips Hue bridge and lights. 
See http://www.meethue.com for more information about these products. It is based on cherrypy, so it will
serve a webpages with information about the lights and options to control them.

HueControl also is a framework for you to create your own plugins.

Dependencies
------------

* Python 2.7 (not tested with 3.0+)


Installation
------------

Just clone, run StartHueControl.py and open the webpage @ http://localhost:8282.
Make sure you run it in the background by running python StartHueControl.py & (include the &).
It then backgrounds the proces and gives you a job number. By doing a fg (jobnr) you get your process back.

Plugins
-------

Included plugins:
* HueControl
    * Index page, allows quick control on your lights)
* AutoOn 
    * Automatically turns on your lights when it gets dark outside (based on sunset times from http://www.earthtools.org)



Writing your own plugins
------------------------

<Placeholder for documentation links and stuff>
For now take a look at plugins/AutoOn and plugins/HueControl.

To do list of things to do:
---------------------------
* Improve and document interfaces to the plugins (HueBridge, Scheduler, Template, ConfigurationServer)
* Group management (create, edit and deletion)
* Better web interface...
* More plugins!
