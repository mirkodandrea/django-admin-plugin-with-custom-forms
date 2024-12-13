from django import forms

class BasePlugin:
    name = "Base Plugin"

    @staticmethod
    def get_form(data=None):
        class PluginForm(forms.Form):
            # Default base form
            example_field = forms.CharField(label="Example", max_length=100, initial=data.get('example_field') if data else '')

        return PluginForm


class PluginA(BasePlugin):
    name = "Plugin A"

    @staticmethod
    def get_form(data=None):
        class PluginAForm(forms.Form):
            field_a = forms.CharField(label="Field A", max_length=100, initial=data.get('field_a') if data else '')
        return PluginAForm


class PluginB(BasePlugin):
    name = "Plugin B"

    @staticmethod
    def get_form(data=None):
        class PluginBForm(forms.Form):
            field_b = forms.IntegerField(label="Field B", initial=data.get('field_b') if data else 0)
        return PluginBForm
    

class PluginC:
    name = "Plugin C"

    @staticmethod
    def get_form(data=None):
        class PluginCForm(forms.Form):
            # Top-level fields
            title = forms.CharField(label="Title", max_length=100, initial=data.get('title') if data else '')

            # Nested fields for an address block
            address__line1 = forms.CharField(label="Address Line 1", max_length=100, initial=data.get('address', {}).get('line1') if data else '')
            address__line2 = forms.CharField(label="Address Line 2", max_length=100, required=False, initial=data.get('address', {}).get('line2') if data else '')
            city = forms.CharField(label="City", max_length=50, initial=data.get('address', {}).get('city') if data else '')
            state = forms.CharField(label="State", max_length=50, initial=data.get('address', {}).get('state') if data else '')
            zip_code = forms.CharField(label="Zip Code", max_length=10, initial=data.get('address', {}).get('zip_code') if data else '')
            triple__nested__field1 = forms.CharField(label="Triple Nested Field", initial=data.get('triple', {}).get('nested', {}).get('field1') if data else '')
            triple__nested__field2 = forms.CharField(label="Triple Nested Field", initial=data.get('triple', {}).get('nested', {}).get('field2') if data else '')

        return PluginCForm


PLUGINS = {
    'PluginA': PluginA,
    'PluginB': PluginB,
    'PluginC': PluginC,
}
