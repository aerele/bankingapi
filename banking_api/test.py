# -*- coding: utf-8 -*-

class Test(object):
	def __init__(self, config=None, use_sandbox = None, proxy_dict = None, file_paths = None, site_path=''):
		self.config = config

	def fetch_balance(self, filters):
		if filters['ACCOUNTNO'] == '1234567890': 
			return {
				"account_no":"1789123456789",
				"date":"18/03/21 10:57:21",
				"currency":"INR",
				"balance":"9356851.92",
				"status":"SUCCESS"}
		return {
			"message":"Invalid account",
			"status":"FAILURE"}

	def fetch_statement(self, filters):
		return {
		'status': 'SUCCESS',
		'record':[{"CHEQUENO":{},
		"TXNDATE":"08-01-2018 13:16:22",
		"REMARKS":"TRFR TO:",
		"AMOUNT":"6,500.00",
		"BALANCE":"2,36,980.40",
		"VALUEDATE":"03-07-2015",
		"TYPE":"DR","TRANSACTIONID":"M328746"},
		{"CHEQUENO":{},
		"TXNDATE":"08-01-2018 13:16:23",
		"REMARKS":"TRFR TO:",
		"AMOUNT":"7,500.00",
		"BALANCE":"2,29,480.40",
		"VALUEDATE":"03-07-2015",
		"TYPE":"DR",
		"TRANSACTIONID":"M328755"}]
		}
	
	def fetch_statement_with_pagination(self, filters):
		return {
		'status': 'SUCCESS',
		'record':[{"CHEQUENO":{},
		"TXNDATE":"08-01-2018 13:16:22",
		"REMARKS":"TRFR TO:",
		"AMOUNT":"6,500.00",
		"BALANCE":"2,36,980.40",
		"VALUEDATE":"03-07-2015",
		"TYPE":"DR","TRANSACTIONID":"M328746"},
		{"CHEQUENO":{},
		"TXNDATE":"08-01-2018 13:16:23",
		"REMARKS":"TRFR TO:",
		"AMOUNT":"7,500.00",
		"BALANCE":"2,29,480.40",
		"VALUEDATE":"03-07-2015",
		"TYPE":"DR",
		"TRANSACTIONID":"M328755"}]
		}

	def initiate_transaction_without_otp(self, filters, transaction_type_mapping):
		if filters["DEBITACC"] == '1234567890':
			return {
			'status': 'SUCCESS',
			'utr_number': '056953631'
				}
		
		if filters["DEBITACC"] == '0123456789':
			return {
			'message': 'Invalid account number',
			'error_code':'100518',
			'status': 'FAILURE'}
		
		if filters["UNIQUEID"] == 'OBP123456':
			return {
				'message':'Same unique id found',
				'error_code':'32432',
				'status': 'DUPLICATE'}
		
		if filters["CREDITACC"] == '123456789':
			return {'message':'Transaction is suspect',
			'error_code':'23213',
			'status': 'PENDING'}
		
		if filters["DEBITACC"] == '1234567890':
			return {'message':'Transaction initiated after CUTOFF',
			'error_code':'23223',
			'status': 'PENDING For Processing'}

	def initiate_transaction_with_otp(self, filters, transaction_type_mapping):
		if filters['OTP'] == 1234:
			return {
			'status': 'SUCCESS',
			'utr_number': '056953631'
				}
		elif filters["DEBITACC"] == '0123456789':
			return {
			'message': 'Invalid account number',
			'error_code':'100518',
			'status': 'FAILURE'}
		elif filters["UNIQUEID"] == 'OBP123456':
			return {
				'message':'Same unique id found',
				'error_code':'32432',
				'status': 'DUPLICATE'}
		elif filters["CREDITACC"] == '123456789':
			return {'message':'Transaction is suspect',
			'error_code':'23213',
			'status': 'PENDING'}
		elif filters["DEBITACC"] == '1234567890':
			return {'message':'Transaction initiated after CUTOFF',
			'error_code':'23223',
			'status': 'PENDING For Processing'}
		else:
			return {
			'message': 'Invalid OTP',
			'error_code':'100518',
			'status': 'FAILURE'}

	def get_transaction_status(self, filters):
		if filters["UNIQUEID"] == 'OBP12345':
			return {
			'message': 'Transaction Failed',
			'error_code':'100518',
			'status': 'FAILURE'}
		
		if filters["UNIQUEID"] == 'OBP123456':
			return {
			'status': 'SUCCESS',
			'utr_number': '056953631'
				}
		if filters["UNIQUEID"] == 'OBP1234567':
			{
				'message':'Same unique id found',
				'error_code':'32432',
				'status': 'DUPLICATE'}
		
		if filters["UNIQUEID"] == 'OBP12345678':
			return {'message':'Transaction is suspect',
			'error_code':'23213',
			'status': 'PENDING'}
		
		if filters["UNIQUEID"] == 'OBP123456789':
			return {'message':'Transaction initiated after CUTOFF',
			'error_code':'23223',
			'status': 'PENDING For Processing'}

	def send_otp(self, filters):
		otp = 1234
		if filters["AMOUNT"] == '1.0':
			return {
				'status': 'SUCCESS',
				'message': 'OTP sent successfully'
			}
		else:
			return {
				'status': 'FAILURE',
				'message': 'Unable to send OTP'
			}