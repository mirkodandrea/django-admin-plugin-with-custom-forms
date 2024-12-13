from django.contrib import admin
from django import forms
from .models import PluginModel
from .plugins import PLUGINS

from django.utils.safestring import mark_safe

class PluginModelForm(forms.ModelForm):
    class Meta:
        model = PluginModel
        fields = ['plugin', 'options']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the options field with JSON or leave it empty.


@admin.register(PluginModel)
class PluginModelAdmin(admin.ModelAdmin):
    form = PluginModelForm
    change_form_template = 'admin/plugins/pluginmodel/change_form.html'

    class Media:
        js = ('plugins/js/plugin_form.js',)
