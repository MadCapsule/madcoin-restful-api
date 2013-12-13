from app import app
import bitcoinrpc
from flask import jsonify
from flask import request
from bitcoinrpc.exceptions import InsufficientFunds

conn = None


@app.route('/connectlocal')
@app.route('/connectlocal/<filename>')
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


@app.route("/connectremote/<user>/<password>/<host>/<int:port>")
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


@app.route("/")
def index():
    """
    Intro message to Madcoin API services.
    """
    resp = jsonify(
        powered_by='Madcapsule Media',
        service='Welcome to Madcoin API services.',
        version=0.1,
        code="1000")
    resp.status_code = 200
    return resp


@app.route("/getinfo")
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


@app.route("/getbalance")
def getbalance():
    """
    Getting the current balance.
    """
    resp = jsonify(balance=conn.getbalance(), code="1000")
    resp.status_code = 200
    return resp


@app.route("/validateaddress/<address>", methods=['POST'])
def validateaddress(address):
    """
    Check a customer address for validity and get information about it.

    @type address: string
    @param address: Coin address to be validated
    """
    rv = conn.validateaddress(address)
    if rv.isvalid:
        resp = jsonify(message="The address that you provided is valid")
        resp.status_code = 200
    else:
        resp = jsonify(message="The address that you provided is invalid, \
            please correct", code="1001")
        resp.status_code = 500
    return resp


@app.route("/sendtoaddress/<address>/<float:amount>", methods=['POST'])
def sendtoaddress(address, amount):
    """
    Sends a specified amount of coins to a specified address.

    @type address: string
    @param address: Address to send the coins
    @type amount: float
    @param amount: Amount to be send
    """
    conn.sendtoaddress(address, amount)
    resp = jsonify(message="Coins sended", code="1000")
    resp.status_code = 200
    return resp


@app.route("/getnewaddress")
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


@app.route("/getreceivedbyaddress/<address>")
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


@app.route("/getreceivedbyaddress/<account_origin>/ \
    <account_dest>/<float:amount>")
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


@app.errorhandler(InsufficientFunds)
def insufficient_funds(error=None):
    message = {'status': 404, 'message': 'Insufficient funds'}
    resp = jsonify(message)
    resp.status_code = 500
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Not Found: ' + request.url}
    resp = jsonify(message)
    resp.status_code = 404
    return resp
