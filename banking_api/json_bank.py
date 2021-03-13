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
				"isPromoCodeValid": false,
				"authenticated": false
			}
		}
		return res["body"]["resultInfo"]["resultStatus"]

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
		return res["body"]["resultInfo"]["resultStatus"]