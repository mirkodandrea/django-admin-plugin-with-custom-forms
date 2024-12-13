from django.db import models
from django.core.exceptions import ValidationError

class PluginModel(models.Model):
    PLUGIN_CHOICES = [
        ('PluginA', 'Plugin A'),
        ('PluginB', 'Plugin B'),
        ('PluginC', 'Plugin C'),
    ]

    plugin = models.CharField(max_length=50, choices=PLUGIN_CHOICES)
    options = models.JSONField(blank=True, null=True)

    def clean(self):
        # Add custom validation if needed
        if self.plugin not in dict(self.PLUGIN_CHOICES):
            raise ValidationError("Invalid plugin selected.")