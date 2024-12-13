from django import forms
from abc import abstractmethod
from django.core.exceptions import ValidationError
from django.utils.html import format_html, format_html_join
from typing import Dict

def flatten_data(data, parent_key='', sep='__'):
    """
    Flatten nested dictionaries into a single level using the given separator.
    """
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_data(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class BasePluginForm(forms.Form):
    @abstractmethod
    def plugin_clean(self, data) -> (Dict[str, str]|None) :
        pass

class BasePlugin:
    @staticmethod
    def get_form() -> BasePluginForm:
        raise NotImplementedError("Subclasses must implement this method.")
    

class SimplePlugin(BasePlugin):
    @staticmethod
    def get_form():
        class SimplePluginForm(BasePluginForm):
            my_field = forms.IntegerField(label="My Field")
        return SimplePluginForm
    

class NestedWithValidationPlugin:
    @staticmethod
    def get_form():
        class NestedPluginForm(BasePluginForm):
            title = forms.CharField(label="Title", max_length=100)
            address__line1 = forms.CharField(label="Address Line 1", max_length=100)
            address__line2 = forms.CharField(label="Address Line 2", max_length=100)
            more__nested__data1 = forms.CharField(label="More Nested Data", max_length=100, initial="Default Value", required=False)
            more__nested__data2 = forms.CharField(label="More Nested Data 2", max_length=100, initial="Default Value", required=False)
            city = forms.CharField(label="City", max_length=50)
            state = forms.CharField(label="State", max_length=50)

            def plugin_clean(self, data) -> Dict[str, str]|None:
                address__line1 = data.get('address__line1', None)
                address__line2 = data.get('address__line2', None)
                
                
                if address__line1 and address__line2 and address__line1 == address__line2:
                    return {
                        'address__line1': 'Address Line 1 and Address Line 2 cannot be the same.'
                    }

        return NestedPluginForm


PLUGINS = {
    'SimplePlugin': SimplePlugin,
    'NestedWithValidationPlugin': NestedWithValidationPlugin,
}
