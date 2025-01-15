from flask import Flask, jsonify, request, render_template

import pprint

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import PaymentTxn
from algosdk.transaction import wait_for_confirmation

# from algosdk.v2client import algod
ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
RECEIVER_ADDRESS = "PB4BVSBFL5XTJSAM2XHGJOUGDPMJHAQ5BSKBNLEPFCN7IU4PHRNUZ2X3AA"
SENDER_ADDRESS = "K6TDRJ36RZRI5KOJ2OBS63MN4BI7D55WH3WCT5WLUWZZA5M7SUOMCKIBAI"
SENDER_MNEMONIC = "eternal wrong caught note notable gaze twice dizzy judge iron love neutral glad strike crime open runway profit dentist already exclude misery test able estate"

def get_wallet_balance(wallet_address):
	"""
	Get the balance of a wallet.

	:param wallet_address: The address of the wallet to check balance for.
	:return: Balance in microAlgos.
	"""
	try:
		# Fetch account information
		account_info = algod_client.account_info(wallet_address)
		balance = account_info.get('amount', 0)  # Get the balance in microAlgos
		print(f"Wallet Address: {wallet_address}")
		print(f"Balance: {balance} microAlgos")
		return balance
	except Exception as e:
		print(f"An error occurred while fetching the wallet balance: {e}")
		return None


def make_txn(sender_mnemonic: str, receiver_address: str, amount: int, is_micro_algos: bool = False):
	"""
	:param sender_mnemonic: 25 word ID.
	:param receiver_address: 58 letter wallet address. i.e 'YQ5NKZMOYRPHVR7R65GTOKNCFIRNDEJDCORMOBK6QRBX5SJCKU4FH35ZH4'
	:param amount: sum to transact in algos. minimum 100_000.
	:param amount: divides amount by 1_000_000.
	"""
	sender_private_key = mnemonic.to_private_key(sender_mnemonic)
	sender_address = account.address_from_private_key(sender_private_key)
	# AMOUNT =   # in microAlgos

	# Suggest parameters from the network
	params = algod_client.suggested_params()

	# Optionally, you can add a note
	note = "Test Payment from user1 to user2".encode()

	# ----------------------------------------------------------------------------
	# 4. CREATE AND SIGN THE TRANSACTION
	# ----------------------------------------------------------------------------
	amount_divisor = 1e6 if is_micro_algos else 1
	amount_in_algos = int(amount / amount_divisor)
	txn = PaymentTxn(
		sender=sender_address,
		sp=params,
		receiver=receiver_address,
		amt=amount_in_algos,
		note=note
	)

	signed_txn = txn.sign(sender_private_key)

	# ----------------------------------------------------------------------------
	# 5. SEND THE TRANSACTION
	# ----------------------------------------------------------------------------
	try:
		txid = algod_client.send_transaction(signed_txn)
		print(f"Transaction sent with TXID: {txid}")
		confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
		print("Transaction confirmed in round:", confirmed_txn.get("confirmed-round", 0))
		return txid

	except Exception as e:
		print(f"Failed to send transaction: {e}")


def print_transaction_info(txid):
	"""
	Get transaction information given a transaction ID.

	:param txid: The transaction ID.
	:return: Transaction information as a dictionary.
	"""
	try:
		# Fetch transaction information
		print()
		transaction_info = algod_client.pending_transaction_info(txid)
		print(f"Transaction Info for TXID {txid}:")
		pprint.pprint(transaction_info)
		print()
		# print(transaction_info)
		return transaction_info
	except Exception as e:
		print(f"An error occurred while fetching transaction info: {e}")
		return None


if __name__ == '__main__':
	pass

# pre_balance = get_wallet_balance(wallet_address=RECEIVER_ADDRESS)
# txid = make_txn(sender_mnemonic=SENDER_MNEMONIC, receiver_address=RECEIVER_ADDRESS, amount=100_000_000, is_micro_algos=False)
# pprint.pprint(print_transaction_info(txid))
# post_balance = get_wallet_balance(wallet_address=RECEIVER_ADDRESS)


app = Flask(__name__)

# Mock data for wallet
wallet = {
	"id": SENDER_ADDRESS,
	"balance": get_wallet_balance(wallet_address=SENDER_ADDRESS)
}

# Mock transactions
transactions = [

]

# Mock items for sale
items = [
	{"name": "Hedwig Pop", "price": 10000000000.00},
	{"name": "Triangles Toaster", "price": 20000000000.00},
	{"name": "Aquarium Filter", "price": 30000000000.00},
	{"name": "Garlic Peel", "price": 40000000000.00},
	{"name": "Dust", "price": 50000000000.00},
]


@app.route('/api/wallet', methods=['GET'])
def get_wallet():
	return jsonify(wallet)


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
	return jsonify(transactions)


@app.route('/api/items', methods=['GET'])
def get_items():
	return jsonify(items)


@app.route('/api/purchase', methods=['POST'])
def purchase_items():
	cart = request.get_json()
	total_cost = sum(items[int(index)]['price'] * quantity for index, quantity in cart.items())
	txid = make_txn(sender_mnemonic=SENDER_MNEMONIC, receiver_address=RECEIVER_ADDRESS, amount=total_cost, is_micro_algos=False)
	wallet['balance'] = get_wallet_balance(wallet_address=SENDER_ADDRESS)
	# Record transaction
	transactions.append(print_transaction_info(txid))

	return jsonify({"success": True, "new_balance": wallet['balance']})


@app.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(debug=True)
