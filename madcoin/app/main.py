import bitcoinrpc
from flask import Flask, jsonify, request
from bitcoinrpc.exceptions import InsufficientFunds
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

#app = Flask(__name__)
__all__ = ['make_json_app']
conn = None

@app.route("/")
def index():
	"""
	Intro message to Madcoin API services.
	"""
	return "<div style='text-align:center'><h1>Welcome to Madcoin API services.</h1><br /><h4>Powered by Madcapsule Media.</h4></div>"

@app.route("/connect_to_local")
def connect_to_local():
	"""
	Connect our system with coind installed in our local host.
	"""
	global conn
	conn = bitcoinrpc.connect_to_local()
	return "Connected!"

@app.route("/connect_to_remote/<host>/<int:port>", methods=['POST'])
def connect_to_remote(host, port):
	global conn
	conn = bitcoinrpc.connect_to_remote('foo', 'bar', host=host, port=port)

@app.route("/get_info")
def get_info():
	"""
	Getting the coin server info.
	"""
	if request_wants_json():
		return jsonify("hola")
	return str(conn.getinfo())

@app.route("/get_balance")
def get_balance():
	"""
	Getting the current balance.
	"""
	conn = bitcoinrpc.connect_to_local()
	return str(conn.getbalance())

@app.route("/validateaddress/<address>", methods=['POST'])
def validateaddress(address):
	"""
	Check a customer address for validity and get information about it.
	"""
	rv = conn.validateaddress(foo)
	if rv.isvalid:
		return true
		#print "The address that you provided is valid"
	else:
		return false
		#print "The address that you provided is invalid, please correct"

@app.route("/sendtoaddress/<address>/<float:amount>", methods=['POST'])
def sendtoaddress(address, amount):
	"""
	Sends a specified amount of coins to a specified address.
	"""
	conn.sendtoaddress(address, amount)

@app.route("/getnewaddress")
def getnewaddress():
	"""
	Get a new address for accepting payments.

	To accept payments, use this method to generate a new address.
	Give this address to the customer and store it in a safe place,
	to be able to check when the payment to this address has been made.
	"""
	return conn.getnewaddress()

@app.route("/getreceivedbyaddress/<address>", methods=['POST'])
def getreceivedbyaddress(address):
	"""
	Check how much has been received at a certain address.

	This method returns how many coins have been received at a certain
	address. Together with the previous function, this can be used to check
	whether a payment has been made by the customer.
	"""
	amount = conn.getreceivedbyaddress(address)
	if request_wants_json():
		return jsonify(amount)
	return amount

@app.route("/getreceivedbyaddress/<account_origin>/<account_dest>/<float:amount>", methods=['POST'])
def move(account_origin, account_dest, amount):
	"""
	Move coins from one account to another account

	Try to move one coins from account_origin to account account_dest
	using move(). Catch the InsufficientFunds exception in the case the
	originating account is broke.
	"""
	try:
		conn.move(account_origin, account_dest, amount)
	except InsufficientFunds,e:
		return str(e)
		#print "Account does not have enough funds available!"

def request_wants_json():
	"""
	If you send an HTTP request to this website it will send you some HTML back
	which your browser will render. However if you provide an Accept header and
	give application/json a higher quality than HTML or any other mimetype (or
	specify it as only accepted mimetype) it will send you back some JSON
	instead.
	
	Why check if json has a higher quality than HTML and not just go with the
	best match? Because some browsers accept on */* and we don't want to deliver
	JSON to an ordinary browser.

	@todo: I recommend implementing to_json methods on your objects that return
	a Python object (dictionary etc.) that can be safely converted to JSON by
	jsonify.
	"""
	best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
	return best == 'application/json' and \
		request.accept_mimetypes[best] > \
		request.accept_mimetypes['text/html']

def make_json_app(import_name, **kwargs):
	"""
	Creates a JSON-oriented Flask app.

	All error responses that you don't specifically
	manage yourself will have application/json content
	type, and will contain JSON like this (just an example):

	{ "message": "405: Method Not Allowed" }
	"""
	def make_json_error(ex):
		response = jsonify(message=str(ex))
		response.status_code = (ex.code
								if isinstance(ex, HTTPException)
								else 500)
		return response

	app = Flask(import_name, **kwargs)

	for code in default_exceptions.iterkeys():
		app.error_handler_spec[None][code] = make_json_error

	return app

if __name__=='__main__':
	connect_to_local() #connect to the local coin daemon
	app.run(debug=True, host='0.0.0.0')
