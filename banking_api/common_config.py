import importlib
class CommonConfig():
    def fetch_balance(provider_name):
        banking_api = get_banking_api_file_path(provider_name)
        bal = banking_api.fetch_balance()
        return bal['EFFECTIVEBAL']
    def fetch_statement(provider_name):
        banking_api = get_banking_api_file_path(provider_name)
        statment = banking_api.fetch_statement()
        return statement
    
def get_banking_api_file_path(provider_name):
    bank_api_file_dict = {'Test': 'test'}
    module_name = '{relative_path}.{module_name}'.format(
                relative_path='banking_api', module_name=bank_api_file_dict[provider_name])
    banking_api = importlib.import_module(module_name)
    return banking_api
