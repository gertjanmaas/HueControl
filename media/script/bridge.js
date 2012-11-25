<%! import cherrypy %>
function set_light(light_name, param, val)
{
    jQuery.ajax( '${cherrypy.url('/plugins/HueControl/control_light/')}' + light_name + '/' + param + '/' + val);
}

function set_group(group_name, param, val)
{
    jQuery.ajax( '${cherrypy.url('/plugins/HueControl/control_group/')}' + group_name + '/' + param + '/' + val);
}