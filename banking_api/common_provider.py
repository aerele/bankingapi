import importlib

def get_provider_class(provider_name):
    provider_file = provider_name.lower().replace(' ','_')
    provider_module = importlib.import_module(f'banking_api.{provider_file}')
    provider_class = getattr(provider_module, provider_name.title().replace(' ',''))
    return provider_class


class CommonProvider(object):
    """
    common provider main class
    """
    def __init__(self, provider, config_info = None):
        """
        Construct a new 'CommonProvider' object.

        :param provider: bank api provider name
        :param config_info: configuration info that is needed for various provider API's function
        """
        self.provider_module = get_provider_class(provider)(config_info)

    def fetch_balance(self):
        return self.provider_module.fetch_balance()

    def fetch_statement(self):
        return self.provider_module.fetch_statement()