from django.http import HttpResponse, JsonResponse
from .plugins import PLUGINS
import json

def dynamic_form(request, plugin_name):
    plugin = PLUGINS.get(plugin_name)
    if not plugin:
        return JsonResponse({'error': 'Invalid plugin'}, status=400)

    form_class = plugin.get_form()
    form = form_class() 
    
    return HttpResponse(form.as_p())  # Render the form for GET requests
