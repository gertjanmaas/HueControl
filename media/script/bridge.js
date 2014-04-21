<%! import cherrypy %>
function set_light(light_name, param, element)
{
    isOn = (element.src.indexOf("icon-light-on") !== -1 ? true: false);
    newState = !isOn;
    jQuery.ajax( '${cherrypy.url('/plugins/HueControl/control_light/')}' + encodeURIComponent(light_name) + '/' + param + '/' + newState);
    if (newState === false) {
        element.src = element.src.replace("icon-light-on", "icon-light-off");
    } else {
        element.src = element.src.replace("icon-light-off", "icon-light-on");
    }
}

function set_group(group_name, param, val)
{
    jQuery.ajax( '${cherrypy.url('/plugins/HueControl/control_group/')}' + encodeURIComponent(group_name) + '/' + param + '/' + val);
}