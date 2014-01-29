import bitcoinrpc
from flask import Flask, Blueprint, current_app, jsonify, request
from flask.ext.cors import cross_origin
from bitcoinrpc.exceptions import InsufficientFunds, JSONTypeError, \
    InvalidAmount


conn = None
server = ""
api = Blueprint('api', __name__)


@api.before_app_request
def before_app_request():
    global server
    print "server: " + server
    print "coin daemon: " + current_app.config['COIN_DAEMOM']

    if conn is None:
        server = current_app.config['COIN_DAEMOM']
        connectlocal(current_app.config['PATH_COIN_CONFIG_FILE'])
    elif server is not current_app.config['COIN_DAEMOM']:
        print "connect"
        server = current_app.config['COIN_DAEMOM']
        connectlocal(current_app.config['PATH_COIN_CONFIG_FILE'])

@api.route("/connectlocal")
@cross_origin()
def connectlocal(filename=None):
    """
    Connect to default coin service instance owned by this user,
    on this machine.

    @type filename: string
    @param filename: Path to a configuration file in a non-standard
    location (optional).
    """
    global conn
    conn = bitcoinrpc.connect_to_local(filename)
    resp = jsonify(message="connected", code="1000")
    resp.status_code = 200
    return resp


@api.route("/connectremote/<user>/<password>/<host>/<int:port>")
@cross_origin()
def connectremote(user, password, host, port):
    """
    Connect to remote or alternative local coin client instance.

    @type user: string
    @param user: Authenticate as user.
    @type password: string
    @param password: Authentication password.
    @type host: string
    @param host: Coin service JSON-RPC host.
    @type port: int
    @param port: Coin service JSON-RPC port.
    """
    global conn
    conn = bitcoinrpc.connect_to_remote(user, password, host=host, port=port)
    resp = jsonify(message="connected", code="1000")
    resp.status_code = 200
    return resp


@api.route("/")
@cross_origin()
def index():
    """
    Intro message to Madcoin API services.
    """
    resp = jsonify(
        powered_by='Madcapsule Media',
        service='Welcome to Madcoin API services.',
        version=0.1,
        coid_daemon=current_app.config['COIN_DAEMOM'],
        code="1000")
    resp.status_code = 200
    return resp


@api.route("/getinfo")
@cross_origin()
def getinfo():
    """
    Getting the coin server info.

    @todo: I recommend implementing to_json methods on your objects that return
    a Python object (dictionary etc.) that can be safely converted to JSON by
    jsonify.
    @todo: There are more info from the coin service that the showed here.
    """
    info = conn.getinfo()
    resp = jsonify(
        errors=info.errors,
        blocks=info.blocks,
        paytxfee=info.paytxfee,
        connections=info.connections,
        difficulty=info.difficulty,
        testnet=info.testnet,
        version=info.version,
        proxy=info.proxy,
        balance=info.balance,
        keypoololdest=info.keypoololdest,
        keypoolsize=info.keypoolsize,
        code="1000")
    resp.status_code = 200
    return resp


@api.route("/getbalance")
@cross_origin()
def getbalance():
    """
    Getting the current balance.
    """
    resp = jsonify(balance=conn.getbalance(), code="1000")
    resp.status_code = 200
    return resp


@api.route("/validateaddress/<address>")
@cross_origin()
def validateaddress(address):
    """
    Check a customer address for validity and get information about it.

    @type address: string
    @param address: Coin address to be validated
    """
    rv = conn.validateaddress(address)
    if rv.isvalid:
        resp = jsonify(message="The address that you provided is \
            valid", code="1000")
        resp.status_code = 200
    else:
        resp = jsonify(message="The address that you provided is invalid, \
            please correct", code="1001")
        resp.status_code = 500
    return resp


@api.route("/sendtoaddress/<address>/<float:amount>")
@cross_origin()
def sendtoaddress(address, amount):
    """
    Sends a specified amount of coins to a specified address.

    @type address: string
    @param address: Address to send the coins
    @type amount: float
    @param amount: Amount to be send
    """
    txid = None
    txid = conn.sendtoaddress(address, amount)
    resp = jsonify(message="Coins sended", txid=txid, code="1000")
    resp.status_code = 200
    return resp


@api.route("/getnewaddress")
@cross_origin()
def getnewaddress():
    """
    Get a new address for accepting payments.

    To accept payments, use this method to generate a new address.
    Give this address to the customer and store it in a safe place,
    to be able to check when the payment to this address has been made.
    """
    resp = jsonify(address=conn.getnewaddress(), code="1000")
    resp.status_code = 200
    return resp


@api.route("/getreceivedbyaddress/<address>")
@cross_origin()
def getreceivedbyaddress(address):
    """
    Check how much has been received at a certain address.

    This method returns how many coins have been received at a certain
    address. Together with the previous function, this can be used to check
    whether a payment has been made by the customer.

    @type address: string
    @param address: Check the balance of the Address
    """
    resp = jsonify(amount=conn.getreceivedbyaddress(address), code="1000")
    resp.status_code = 200
    return resp


@api.route("/move/<account_origin>/<account_dest>/<float:amount>")
@cross_origin()
def move(account_origin, account_dest, amount):
    """
    Move coins from one account to another account

    Try to move one coins from account_origin to account account_dest
    using move(). Catch the InsufficientFunds exception in the case the
    originating account is broke.

    @type account_origin: string
    @param account_origin: Check the balance of the Address
    @type account_dest: string
    @param account_dest: Check the balance of the Address
    @type amount: float
    @param amount: Check the balance of the Address
    @todo: We have to check first if the accounts exists
    """
    try:
        conn.move(account_origin, account_dest, amount)
    except InsufficientFunds:
        resp = jsonify(message="Account does not have enough funds  \
            available!", code="1002")
        resp.status_code = 500
        return resp

    resp = jsonify(message="Coins moved", code="1000")
    resp.status_code = 200
    return resp


@api.errorhandler(InsufficientFunds)
def insufficient_funds(error=None):
    message = {'status': 404, 'message': 'Insufficient funds'}
    resp = jsonify(message)
    resp.status_code = 500
    return resp


@api.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Not Found: ' + request.url}
    resp = jsonify(message)
    resp.status_code = 404
    return resp
