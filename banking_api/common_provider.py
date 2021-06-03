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
	def __init__(self, provider, config = None, use_sandbox = None, proxy_dict = None, file_paths = None, site_path = None):

		# config = {"APIKEY": "i1431423123123123",
		# 		"CORPID":"Test45",
		# 		"USERID":"USER3",
		# 		"AGGRID":"IT56754",
		# 		"AGGRNAME":"TEST",
		# 		"URN": "ERTERT345634"}

		#use_sandbox = 0

		# proxy_dict= {"http":"http://13.08.195.295:3001",
		# 		"https":"https://13.08.195.295:3001",
		# 		"ftp":"ftp://13.08.195.295:3001"}

		# file_paths = {'private_key': 'test/private_key.pem',
		# 			  'public_key': 'test/public_key.pem'}

		"""
		Construct a new 'CommonProvider' object.

		:param provider: bank api provider name
		:param config: pass credentials that is needed for specific provider
		:param use_sandbox: pass 1 for sandbox env and 0 for live env
		:param proxy_dict: proxy details with ip and port as dict
		:param file_paths: private and public key file paths
		:param site_path: site path
		"""
		self.transaction_type_mapping = {	
			'ICICI': {'RTGS': 'RTG', 'NEFT': 'RGS', 'IMPS': 'IFS',	
			'Internal Payments': 'OWN', 'External Payments': 'TPA',	
			'Virtual A/c Payments': 'VAP'	
			},
			'Test': {'RTGS': 'RTG', 'NEFT': 'RGS', 'IMPS': 'IFS',	
			'Internal Payments': 'OWN', 'External Payments': 'TPA',	
			'Virtual A/c Payments': 'VAP'	
			}	
		}	
		self.provider = provider
		self.provider_module = get_provider_class(provider)(config, use_sandbox, proxy_dict, file_paths, site_path)

	def fetch_balance(self, filters):
		return self.provider_module.fetch_balance(filters)

	def fetch_statement(self, filters):
		return self.provider_module.fetch_statement(filters)

	def initiate_transaction_without_otp(self, filters):
		return self.provider_module.initiate_transaction_without_otp(filters, self.transaction_type_mapping[self.provider])

	def initiate_transaction_with_otp(self, filters):
		return self.provider_module.initiate_transaction_with_otp(filters, self.transaction_type_mapping[self.provider])

	def send_otp(self, filters):
		return self.provider_module.send_otp(filters)

	def get_transaction_status(self, filters):
		return self.provider_module.get_transaction_status(filters)