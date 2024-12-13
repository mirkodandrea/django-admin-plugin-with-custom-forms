from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html, format_html_join

from plugins.plugins import flatten_data
from plugins.plugins import PLUGINS

class PluginModel(models.Model):
    PLUGIN_CHOICES = [(key, key) for key in PLUGINS.keys()]

    plugin = models.CharField(max_length=50, choices=PLUGIN_CHOICES)
    options = models.JSONField(blank=True, null=True)

    def clean(self):
        super().clean()
        # Fetch the plugin and its form
        plugin = PLUGINS.get(self.plugin)
        if not plugin:
            raise ValidationError(f"Plugin '{self.plugin}' is not valid.")

        flatten_options = flatten_data(self.options)
        
        validation_errors = {}
        # validate the options field for every field in the form class
        form_class = plugin.get_form()
        plugin_form = form_class()
        for name, field in plugin_form.fields.items():
            try:
                field.clean(flatten_options.get(name))
            except ValidationError as e:
                #self.add_error(name, e)
                validation_errors[name] = e.message

        other_errors = plugin_form.plugin_clean(flatten_options)
        if other_errors:
            validation_errors.update(other_errors)
        
        if len(validation_errors.keys()) > 0:
            formatted_errors = format_html_join(
                '',
                '<li>{}: {}</li>',
                ((field, error) for field, error in validation_errors.items())
            )
            raise ValidationError(
                format_html(
                    "Invalid options for plugin '{}':<ul>{}</ul>",
                    self.plugin,
                    formatted_errors,
                )
            )

        
    def save(self, *args, **kwargs):
        # flattern the options field           
        super().save(*args, **kwargs)
