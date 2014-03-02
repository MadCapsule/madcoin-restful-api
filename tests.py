import os
import sys
import unittest

import json
import requests

from bitcoinrpc.exceptions import InsufficientFunds

class TestCase(unittest.TestCase):
	def setUp(self):
		data = requests.get('http://127.0.0.1:5000/connectlocal').json()
		assert data['code'] == '1000'

	def test_new_address(self):
		data = requests.get('http://127.0.0.1:5000/getnewaddress').json()
		assert len(data['address']) >= 25 & len(data['address']) <= 34

	def test_send_coins(self):
		global test_address

		data_addr = requests.get('http://127.0.0.1:5000/getnewaddress').json()
		data_send = requests.get('http://127.0.0.1:5000/sendtoaddress/' + data_addr['address'] + '/0.0001').json()
		data_check = requests.get('http://127.0.0.1:5000/getreceivedbyaddress/' + data_addr['address']).json()
		
		# if you wanna check the results
		# print(data_addr)
		# print(data_send)
		# print(data_check)

		assert data_addr['code'] == '1000'
		assert data_send['code'] == '1000'
		assert data_check['code'] == '1000'

if __name__ == '__main__':
    unittest.main()
