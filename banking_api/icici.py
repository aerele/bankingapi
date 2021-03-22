# -*- coding: utf-8 -*-
import requests
import json
import base64
import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Cipher import AES
import Crypto.Cipher.AES
import Crypto.Random


class Icici(object):
	def __init__(self, config=None, use_sandbox = None, proxy_dict = None, file_paths = None):

		# txn_details = { "UNIQUEID": "BOBP2021035678",
		# 				"IFSC":"ICIC736893",
		# 				"AMOUNT":"1",
		# 				"CURRENCY":"INR",
		# 				"TXNTYPE":"TPA",
		# 				"PAYEENAME":"TEST",
		# 				"DEBITACC":"0582438948528",
		# 				"CREDITACC":"90345435988934",
		# 				"WORKFLOW_REQD":"N",
		# 				"ACCOUNTNO": "000405785761611",
		# 				"FROMDATE": "01-07-2015",
		# 				"TODATE":"01-12-2015"}

		"""
		:param config: APIKEY, PRIVATEKEYPATH, CORPID, USERID, AGGRID, AGGRNAME, 
		"""
		self.api_key = config.pop('APIKEY')
		self.config = config
		self.file_paths = file_paths
		self.proxy_dict = proxy_dict
		self.get_headers()

		# url dict for sandbox & live
		if use_sandbox:
			self.urls =  [
				'https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/BalanceInquiry',
				'https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/AccountStatement',
				'https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/Transaction',
				'https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/TransactionInquiry'
				]

	def get_headers(self):
		header = {}
		header["accept"] = "*/*"
		header["content-length"] = "684"
		header["content-type"] = "text/plain"
		header["apikey"] = self.api_key
		self.header = header

	def generate_aes_key(self):
		rnd = Crypto.Random.OSRNG.posix.new().read(AES.block_size)
		return rnd

	def bank_statement_decrypted_response(self):
		response ={}
		Enckey = base64.b64decode(response['encryptedKey'])
		Deckey = cipher.decrypt(Enckey, b'x')
		encData = base64.b64decode(response['encryptedData']); 
		IV = generate_aes_key()
		decipher = AES.new(Deckey, AES.MODE_CBC, IV)
		plaintext = decipher.decrypt(encData)
		return plaintext

	def get_decrypted_response(self, response):
		rsa_key = RSA.importKey(open(self.file_paths['private_key'], "rb").read())
		cipher = Cipher_PKCS1_v1_5.new(rsa_key)
		raw_cipher_data = base64.b64decode(response)
		decrypted_res = cipher.decrypt(raw_cipher_data, b'x')
		return decrypted_res

	def get_encrypted_request(self, params):
		source = json.dumps(params)
		key = RSA.importKey(open(self.file_paths['public_key']).read())

		cipher = Cipher_PKCS1_v1_5.new(key)
		cipher_text = cipher.encrypt(source.encode())
		cipher_text = base64.b64encode(cipher_text)

		return cipher_text

	def send_request(self, url_id, cipher_text):
		if self.proxy_dict:
			response = requests.request("POST", self.urls[url_id], headers=self.headers, data=cipher_text, proxies=self.proxy_dict)
		else:
			response = requests.request("POST", self.urls[url_id], headers=self.headers, data=cipher_text)

		return response
		

	def fetch_balance(self):
		params = self.config
		params.pop('AGGRNAME')
		cipher_text = self.get_encrypted_request(params)
		response = self.send_request(0, cipher_text)
		if response.status_code == 200:
			decrypted_res = self.get_decrypted_response(response)
			return json.dumps(decrypted_res, indent=4, sort_keys=False))
		else:
			return str(response.content)
		


	def fetch_statement(self, filters):
		params = self.config
		params.pop('AGGRNAME')
		params.update(filters)
		cipher_text = self.get_encrypted_request(params)
		response = self.send_request(1, cipher_text)
		if response.status_code == 200:
			decrypted_res = self.bank_statement_decrypted_response(response)
			return json.dumps(decrypted_res, indent=4, sort_keys=False))
		else:
			return str(response.content)

	

	def initiate_transaction(self, filters):
		params = self.config
		params.update(filters)
		cipher_text = self.get_encrypted_request(params)
		response = self.send_request(1, cipher_text)
		if response.status_code == 200:
			decrypted_res = self.bank_statement_decrypted_response(response)
			return json.dumps(decrypted_res, indent=4, sort_keys=False))
		else:
			return str(response.content)


	def get_transaction_status(self, filters):
		params = self.config
		params.pop('AGGRNAME')
		params.update(filters)
		cipher_text = self.get_encrypted_request(params)
		response = self.send_request(3, cipher_text)
		if response.status_code == 200:
			decrypted_res = self.get_decrypted_response(response)
			return json.dumps(decrypted_res, indent=4, sort_keys=False))
		else:
			return str(response.content)