from django.http import HttpResponse
from .plugins import PLUGINS

def dynamic_form(request, plugin_name):
    plugin = PLUGINS.get(plugin_name)
    if plugin:
        form = plugin.get_form()
        return HttpResponse(form().as_p())
    return HttpResponse('<p>Invalid plugin</p>', status=400)
