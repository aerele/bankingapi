# -*- coding: utf-8 -*-
import requests
import json
import PaytmChecksum
import secrets

class JsonBank(object):
	def __init__(self, config=None):
		"""
		:param config: merchant_id, order_id, user_info, txn_info
		"""
		self.config = config
	
	def intiate_transaction(self):
		res = {
			 "head": {
		 		"responseTimestamp": "1526969112101",
		 		"version": "v1",
		 		"clientId": "C11",
		 		"signature": "TXBw50YPUKIgJd8gR8RpZuOMZ+csvCT7i0/YXmG//J8+BpFdY5goPBiLAkCzKlCkOvAQip/Op5aD6Vs+cNUTjFmC55JBxvp7WunZ45Ke2q0="
			 	},
			 "body": {
			 	"resultInfo": {
			 	"resultStatus": "S",
			 	"resultCode": "0000",
			 	"resultMsg": "Success"
			 	},
			 	"txnToken": "fe795335ed3049c78a57271075f2199e1526969112097",
			 	"isPromoCodeValid": false,
			 	"authenticated": false
			 	}
		}
		return res["body"]["resultInfo"]["resultStatus"]

	def transaction_status(self):
		res = {
			"head": {
				"responseTimestamp": "1553496322922",
				"version": "v1",
				"clientId": "C11",
				"signature": "xxxxx"
			},
			"body": {
				"resultInfo": {
					"resultStatus": "TXN_SUCCESS",
					"resultCode": "01",
					"resultMsg": "Txn Success"
				},
				"txnId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
				"bankTxnId": "xxxxxxxxxxxxxxx",
				"orderId": "xxxxxxx",
				"txnAmount": "100.00",
				"txnType": "SALE",
				"gatewayName": "HDFC",
				"bankName": "HSBC",
				"mid": "xxxxxxxxxxxxxxxxxxxx",
				"paymentMode": "CC",
				"refundAmt": "100.00",
				"txnDate": "2019-02-20 12:35:20.0"
			}
			} 
		return res["body"]["resultInfo"]["resultStatus"]