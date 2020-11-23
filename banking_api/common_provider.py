import importlib

def get_provider_class(provider_name):
    provider_file_dict = {'Test': ['test','Test']}
    if provider_name in provider_file_dict:
        provider_module = importlib.import_module(f'banking_api.{provider_file_dict[provider_name][0]}')
        provider_class = getattr(provider_module, provider_file_dict[provider_name][1])
        return provider_class
    raise Exception("No implementation found for the given provider")


class CommonProvider(object):
    """
    common provider main class
    """
    def __init__(self, provider):
        """
        Construct a new 'CommonProvider' object.

        :param provider: bank api provider name
        """
        self.provider_module = get_provider_class(provider)()

    def fetch_balance(self):
        return self.provider_module.fetch_balance()

    def fetch_statement(self):
        return self.provider_module.fetch_statement()