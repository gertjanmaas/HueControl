<%! import cherrypy %>
function set_light(light_name, param, val)
{
    jQuery.ajax( '${cherrypy.url('/plugins/HueControl/control_light/')}' + encodeURIComponent(light_name) + '/' + param + '/' + val);
}

function set_group(group_name, param, val)
{
    jQuery.ajax( '${cherrypy.url('/plugins/HueControl/control_group/')}' + encodeURIComponent(group_name) + '/' + param + '/' + val);
}