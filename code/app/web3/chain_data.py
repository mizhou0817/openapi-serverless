from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_abi import decode
from datetime import datetime
import time
from threading import Thread
from app import app
from app.models.transaction import TransactionModel
from app.models.ether_address import EtherAddressModel
import schedule


class BlockchainEventListener:
    def __init__(self, network_name, rpc_url, tokens):
        self.network_name = network_name
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.tokens = tokens
        self.event_filter = None

        if not self.web3.is_connected():
            raise Exception(f"Failed to connect to {network_name} node")

        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.setup_event_filter()

    def setup_event_filter(self):
        transfer_event_signature = self.web3.keccak(text="Transfer(address,address,uint256)").hex()
        self.event_filter = self.web3.eth.filter({
            "address": [token['contract_address'] for token in self.tokens],
            "topics": [transfer_event_signature]
        })

    def handle_event(self, event, address_list):
        from_address = self.web3.to_checksum_address(event.topics[1].hex()[-40:])
        # to_address = self.web3.to_checksum_address(event.topics[2].hex()[-40:])
        to_address = "0xDf37b75345536F73976311FF86e97b51d299D21F"
        if not self.chack_to_address(to_address, address_list): return
        value = decode(['uint256'], event.data)[0]
        event_details = {
            "contract_address": event.address,
            "transaction_hash": event.transactionHash.hex(),
            "log_index": event.logIndex,
            "block_hash": event.blockHash.hex(),
            "from_address": from_address,
            "to_address": to_address,
            "value": value,
            "network": self.network_name
        }
        token_details = next((token for token in self.tokens if token["contract_address"] == event.address), None)
        combined_details = {**event_details, **token_details}
        combined_details["value"] = combined_details["value"] / (10 ** combined_details["decimals"])
        with app.app_context():
            combined_details["user_id"] = EtherAddressModel.get_user_id_by_address(to_address).user_id
            TransactionModel.create_transaction(combined_details)

    # Check if to_address is in address_list
    # TODO: use redis set
    def chack_to_address(self, to_address, address_list):
        if to_address in address_list:
            print("to_address:", to_address)
            return True
        else:
            return False

    def get_address_list(self):
        with app.app_context():
            return EtherAddressModel.get_all_address()

    def log_loop(self, poll_interval):
        while True:
            address_list = self.get_address_list()
            for event in self.event_filter.get_new_entries():
                self.handle_event(event, address_list)
            time.sleep(poll_interval)

    def get_transaction_details(self, tx_hash):
        try:
            transaction = self.web3.eth.get_transaction(tx_hash)
            receipt = self.web3.eth.get_transaction_receipt(tx_hash)
            if transaction and receipt:
                current_block = self.web3.eth.block_number
                block = self.web3.eth.get_block(transaction['blockNumber'])
                tx_details = {
                    "transaction_hash": transaction.hash.hex(),
                    "from_address": transaction["from"],
                    "to_address": transaction["to"],
                    "block_number": transaction["blockNumber"],
                    "status": receipt["status"],
                    "tx_timestamp": datetime.utcfromtimestamp(block['timestamp']),
                    "confirmations": current_block - transaction['blockNumber']
                }
                with app.app_context():
                    TransactionModel.create_transaction(tx_details)
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def update_latest_confirmation(self):
        with app.app_context():
            pending_tx = TransactionModel.get_pending_tx()
            if pending_tx:
                self.get_transaction_details(pending_tx.transaction_hash)

    def schedule_tasks(self, interval):
        schedule.every(interval).seconds.do(self.update_latest_confirmation)
        while True:
            schedule.run_pending()
            time.sleep(1)


def start_listener(network_name, rpc_url, tokens):
    listener = BlockchainEventListener(network_name, rpc_url, tokens)
    Thread(target=listener.log_loop, args=(2,)).start()
    Thread(target=listener.schedule_tasks, args=(10,)).start()  # Set interval as 5 minutes for example


bsc_tokens = [
    {
        "name": "Tether USD",
        "symbol": "USDT",
        "contract_address": Web3.to_checksum_address("0x55d398326f99059ff775485246999027b3197955"),
        "decimals": 18,
    },
    {
        "name": "USD Coin",
        "symbol": "USDC",
        "contract_address": Web3.to_checksum_address("0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"),
        "decimals": 18,
    }
]

start_listener("BSC", "https://bsc.rpc.blxrbdn.com", bsc_tokens)

# network_name = "BSC"
# rpc_url = "https://bsc.rpc.blxrbdn.com"
# tokens = bsc_tokens
# listener = BlockchainEventListener(network_name, rpc_url, tokens)
# listener.log_loop(2)
