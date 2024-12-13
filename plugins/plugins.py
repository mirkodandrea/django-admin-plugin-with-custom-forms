from django import forms
from abc import abstractmethod, ABC
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

class BasePlugin(ABC):
    @staticmethod
    def get_form() -> BasePluginForm:
        raise NotImplementedError("Subclasses must implement this method.")
    

class SimplePlugin(BasePlugin):
    @staticmethod
    def get_form():
        class SimplePluginForm(BasePluginForm):
            my_field = forms.IntegerField(label="My Field")
        return SimplePluginForm
    
class SSHConnectionPlugin:
    @staticmethod
    def get_form():
        class SSHConnectionForm(BasePluginForm):
            host__hostname = forms.CharField(label="Hostname", max_length=100)
            host__port = forms.IntegerField(label="Port", initial=22)
            username = forms.CharField(label="Username", max_length=100)
            password = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)
            private_key = forms.CharField(label="Private Key", widget=forms.Textarea, required=False)

            def plugin_clean(self, data) -> Dict[str, str] | None:
                password = data.get('password')
                private_key = data.get('private_key')

                errors = {}
                if not password and not private_key:
                    errors['password'] = 'Either password or private key is required.'

                return errors if errors else None

        return SSHConnectionForm

    def __init__(self, options):
        host = options.get('host')
        if not host:
            raise ValueError("Host is required.")
        
        self.hostname = host.get('hostname', None)
        self.port = host.get('port', None)

        self.username = options.get('username')
        self.password = options.get('password')
        self.private_key = options.get('private_key')

    def download(self, remote_path, local_path):
        # Connect to the SSH server using the provided credentials
        pass

class HTTPConnectionPlugin:
    @staticmethod
    def get_form():
        class HTTPConnectionForm(BasePluginForm):
            url = forms.URLField(label="URL")
            port = forms.IntegerField(label="Port", initial=80)
            auth_type = forms.ChoiceField(label="Auth Type", choices=[('none', 'None'), ('basic', 'Basic'), ('token', 'Token')])
            username = forms.CharField(label="Username", max_length=100, required=False)
            password = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)
            token = forms.CharField(label="Token", widget=forms.Textarea, required=False, initial=None)

            def plugin_clean(self, data) -> Dict[str, str] | None:
                auth_type = data.get('auth_type')
                username = data.get('username')
                password = data.get('password')
                token = data.get('token')

                errors = {}
                if auth_type == 'basic' and (not username or not password):
                    errors['auth_type'] = 'Username and password are required for basic authentication.'
                elif auth_type == 'token' and not token:
                    errors['auth_type'] = 'Token is required for token authentication.'

                return errors if errors else None

        return HTTPConnectionForm

    def __init__(self, options):
        self.url = options.get('url')
        self.port = options.get('port')
        self.auth_type = options.get('auth_type')
        self.username = options.get('username')
        self.password = options.get('password')
        self.token = options.get('token')

    def download(self, remote_path, local_path):
        # Connect to the HTTP server using the provided credentials
        pass

PLUGINS = {
    'SimplePlugin': SimplePlugin,
    'SSHConnectionPlugin': SSHConnectionPlugin,
    'HTTPConnectionPlugin': HTTPConnectionPlugin,
}
