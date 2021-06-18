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
	def __init__(self, config=None, use_sandbox = None, proxy_dict = None, file_paths = None, site_path=''):

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
		self.site_path = site_path
		self.params = ''
		self.proxy_dict = proxy_dict
		self.get_headers()

		# url dict for sandbox & live
		# add transaction with otp api endpoint - 4th index
		# add send otp api endpoint	- 5th index
		# add account statement pagination api endpoint - 6th index
		if use_sandbox:
			self.urls =  [
				'https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/BalanceInquiry',
				'https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/AccountStatement',
				'https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/Transaction',
				'https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/TransactionInquiry'
				]
		else:
			self.urls = [
				'https://apibankingone.icicibank.com/api/Corporate/CIB/v1/BalanceInquiry',
				'https://apibankingone.icicibank.com/api/Corporate/CIB/v1/AccountStatement',
				'https://apibankingone.icicibank.com/api/Corporate/CIB/v1/Transaction',
				'https://apibankingone.icicibank.com/api/Corporate/CIB/v1/TransactionInquiry'
				]

	def get_headers(self):
		headers = {}
		headers["accept"] = "*/*"
		headers["content-length"] = "684"
		headers["content-type"] = "text/plain"
		headers["apikey"] = self.api_key
		self.headers = headers

	def generate_aes_key(self):
		rnd = Crypto.Random.OSRNG.posix.new().read(AES.block_size)
		return rnd

	def bank_statement_decrypted_response(self, response):
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
		try:
			raw_cipher_data = base64.b64decode(response.content)
		except:
			raise Exception(f"Invalid Response {response.content}")
		decrypted_res = cipher.decrypt(raw_cipher_data, b'x')
		decrypted_res = decrypted_res.decode("utf-8") 
		return json.loads(decrypted_res)

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


	def fetch_balance(self, filters):
		params = self.config
		params.pop('AGGRNAME')
		params.update(filters)
		self.params = params
		cipher_text = self.get_encrypted_request(params)
		response = self.send_request(0, cipher_text)
		if response.status_code == 200:
			decrypted_res = self.get_decrypted_response(response)
			final_res = {}
			if 'RESPONSE' in decrypted_res:
				final_res ['status'] = decrypted_res['RESPONSE'].upper()
			if 'ACCOUNTNO' in decrypted_res:
				final_res['account_no'] =  decrypted_res['ACCOUNTNO']
			if 'DATE' in decrypted_res:
				final_res['date'] =  decrypted_res['DATE']
			if 'CURRENCY' in decrypted_res:
				final_res['currency'] =  decrypted_res['CURRENCY']
			if 'EFFECTIVEBAL' in decrypted_res:
				final_res['balance'] =  decrypted_res['EFFECTIVEBAL']
			if 'MESSAGE' in decrypted_res:
				final_res['message'] = decrypted_res['MESSAGE']
			return final_res
		else:
			raise Exception(response.content)

	def fetch_statement(self, filters):
		params = self.config
		params.pop('AGGRNAME')
		params.update(filters)
		cipher_text = self.get_encrypted_request(params)
		response = self.send_request(1, cipher_text)
		if response.status_code == 200:
			decrypted_res = self.bank_statement_decrypted_response(response)
			return json.dumps(json.loads(decrypted_res), indent=4, sort_keys=False)
		else:
			return json.dumps(json.loads(response.content), indent=4, sort_keys=False)

	

	def initiate_transaction_without_otp(self, filters, transaction_type_mapping):
		params = self.config
		params.update(filters)
		self.params = params
		filters['TXNTYPE'] = transaction_type_mapping[filters['TXNTYPE']]	
		cipher_text = self.get_encrypted_request(params)
		response = self.send_request(2, cipher_text)
		if response.status_code == 200:
			decrypted_res = self.get_decrypted_response(response)
			final_res = {}
			if 'STATUS' in decrypted_res:
				final_res ['status'] = decrypted_res['STATUS'].upper()
			if 'UTRNUMBER' in decrypted_res:
				final_res['utr_number'] =  decrypted_res['UTRNUMBER']
			if 'MESSAGE' in decrypted_res:
				final_res['message'] = decrypted_res['MESSAGE']
			if 'ERRORCODE' in decrypted_res:
				final_res['error_code'] = decrypted_res['ERRORCODE']
			return final_res
		else:
			raise Exception(response.content)

	def initiate_transaction_with_otp(self, filters, transaction_type_mapping):
		params = self.config
		filters['TXNTYPE'] = transaction_type_mapping[filters['TXNTYPE']]
		params.update(filters)
		self.params = params
		cipher_text = self.get_encrypted_request(params)
		response = self.send_request(4, cipher_text)
		if response.status_code == 200:
			decrypted_res = self.get_decrypted_response(response)
			final_res = {}
			if 'STATUS' in decrypted_res:
				final_res ['status'] = decrypted_res['STATUS'].upper()
			if 'UTRNUMBER' in decrypted_res:
				final_res['utr_number'] =  decrypted_res['UTRNUMBER']
			if 'MESSAGE' in decrypted_res:
				final_res['message'] = decrypted_res['MESSAGE']
				if decrypted_res['MESSAGE'] in ['994006']:
					final_res ['status'] = 'INVALID OTP'
				if decrypted_res['MESSAGE'] in ['107889']:
					final_res ['status'] = 'OTP EXPIRED'
			if 'ERRORCODE' in decrypted_res:
				final_res['error_code'] = decrypted_res['ERRORCODE']
			return final_res
		else:
			raise Exception(response.content)

	def get_transaction_status(self, filters):
		params = self.config
		params.pop('AGGRNAME')
		params.update(filters)
		cipher_text = self.get_encrypted_request(params)
		response = self.send_request(3, cipher_text)
		if response.status_code == 200:
			decrypted_res = self.get_decrypted_response(response)
			final_res = {}
			if 'STATUS' in decrypted_res:
				final_res ['status'] = decrypted_res['STATUS']
			if 'UTRNUMBER' in decrypted_res:
				final_res['utr_number'] =  decrypted_res['UTRNUMBER']
			if 'MESSAGE' in decrypted_res:
				final_res['message'] = decrypted_res['MESSAGE']
			return final_res
		else:
			raise Exception(response.content)

	def send_otp(self, filters):
		params = self.config
		params.update(filters)
		self.params = params
		cipher_text = self.get_encrypted_request(params)
		response = self.send_request(5, cipher_text)
		if response.status_code == 200:
			decrypted_res = self.get_decrypted_response(response)
			final_res = {}
			if 'RESPONSE' in decrypted_res:
				final_res ['status'] = decrypted_res['RESPONSE'].upper()
			if 'MESSAGE' in decrypted_res:
				final_res['message'] = decrypted_res['MESSAGE']
			return final_res
		else:
			raise Exception(response.content)