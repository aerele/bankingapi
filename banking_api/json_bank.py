# -*- coding: utf-8 -*-
import requests
import json
import PaytmChecksum
import secrets

class JsonBank(object):
	def __init__(self, config):
		"""
		:param config: merchant_id, order_id, txn_info
		"""
		self.config = config
	
	def generate_order_id(self):
		id = '{:0>4}'.format(secrets.randbelow(10**4))
		return f'OREDRID_{id}'

	def intiate_transaction(self):
		paytmParams = dict()
		order_id = self.generate_order_id()
		paytmParams["body"] = {
		"requestType": "Payment",
	 	"mid": self.config['merchant_id'],
		"websiteName": "WEBSTAGING",
		"orderId": order_id,
		"callbackUrl": "https://merchant.com/callback",
		"txnAmount": {"value": self.config['txn_info']['amount'],
		"currency": "INR"},
		"userInfo": {"custId": self.config['txn_info']['cust_id']}
		}
		checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), self.config['merchant_id'])
		paytmParams["head"] = {"signature": checksum}
		post_data = json.dumps(paytmParams)
		# for Staging
		url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={self.config['merchant_id']}&orderId={order_id}"
		response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
		return response

	# def transaction_status(self):
	# 	paytmParams = dict()

	# 	paytmParams["body"] = {

	# 		"mid" : "YOUR_MID_HERE",
	# 		"orderId" : "YOUR_ORDER_ID",
	# 	}
	# 	checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "YOUR_MERCHANT_KEY")
	# 	paytmParams["head"] = {

	# 		"signature"	: checksum
	# 	}
	# 	post_data = json.dumps(paytmParams)

	# 	# for Staging
	# 	url = "https://securegw-stage.paytm.in/v3/order/status"
	# 	response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
	# 	return response

