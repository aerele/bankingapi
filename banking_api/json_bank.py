# -*- coding: utf-8 -*-
import requests
import json

class JsonBank(object):
	def __init__(self, config=None):
		"""
		:param config: merchant_id, order_id, user_info, txn_info
		"""
		self.config = config
	
	def initiate_transaction(self):
		res = {
			"head": {
				"responseTimestamp": "152696112101",
				"version": "v1",
				"clientId": "C11",
				"signature": "TXBw50YPUK///fwefewegegre"
			},
			"body":{
				"resultInfo":{
					"resultStatus": "S",
					"resultCode": "0000",
					"resultMsg": "Success"
				},
				"txnToken": "fe8798999efewf889090erfre",
				"isPromoCodeValid": False,
				"authenticated": False
			}
		}
		result = {'msg': res["body"]["resultInfo"]["resultMsg"]}
		if res["body"]["resultInfo"]["resultStatus"] == 'S':
			result['status'] == 'Success'
		if res["body"]["resultInfo"]["resultStatus"] == 'F':
			result['status'] == 'Failed'
		if res["body"]["resultInfo"]["resultStatus"] == 'U':
			result['status'] == 'Error'
		return result

	def get_transaction_status(self):
		res = {
			"head": {
				"responseTimestamp": "152696112101",
				"version": "v1",
				"clientId": "C11",
				"signature": "TXBw50YPUK///fwefewegegre"
			},
			"body": {
				"resultInfo":{
					"resultStatus": "TXN_SUCCESS",
					"resultCode": "01",
					"resultMsg": "Txn Success"
				},
				"txnId": "xxxxxxxxxxxxxxxxxxxxxxxxx",
				"bankTxnId": "xxxxxxxxxx",
				"orderId": "xxxxxxxx",
				"txnAmount": "100.00",
				"txnType": "SALE",
				"gatewayName": "HDFC",
				"bankName": "HSBC",
				"mid": "xxxxxxxxxxxxxx",
				"paymentMode": "CC",
				"refundAmt": "100.00",
				"txnDate": "2019-02-20 12:35:20.0"
			}
		}
		result = {'msg': res["body"]["resultInfo"]["resultMsg"]}
		if res["body"]["resultInfo"]["resultStatus"] == 'TXN_SUCCESS':
			result['status'] == 'Success'
		if res["body"]["resultInfo"]["resultStatus"] == 'TXN_FAILURE':
			result['status'] == 'Failed'
		if res["body"]["resultInfo"]["resultStatus"] == 'PENDING':
			result['status'] == 'Pending'
		return result