import os
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc

import sys

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '0.0.0.0')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@mchain')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', '505e3ee6da65ad07268236e49a302d982c027e353ee9bd0acb89b2c395151deb')

user_private_key = IrohaCrypto.private_key()
user_public_key = IrohaCrypto.derive_public_key(user_private_key)
iroha = Iroha('admin@mchain')
net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))


def add_coin_to_admin():
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id='coin#domain', amount='1000.00')
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


def create_account(signin_name,pub_key):
    tx = iroha.transaction([
        iroha.command('CreateAccount', account_name=signin_name, domain_id='mchain',
                      public_key=pub_key)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    net.send_tx(tx)


def transfer_coin_from_admin_to_user(acc_id,amt):
    tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id='admin@mchain', dest_account_id=acc_id+'@mchain',
                      asset_id='coin#mchain', amount=amt)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    net.send_tx(tx)


def get_account_assets(acc_name):
    """
    List all the assets of userone@domain
    """
    acc_id = acc_name + '@mchain'
    query = iroha.query('GetAccountAssets', account_id=acc_id)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

    response = net.send_query(query)
    data = response.account_assets_response.account_assets

    return data


def get_asset_transaction(acc_id,asset):
    query = iroha.query('GetAccountAssetTransactions', account_id= acc_id+'@mchain', asset_id=asset+'#mchain', page_size= 5)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    response = net.send_query(query)
    result = response.transactions_page_response.transactions
    return result


def get_userone_details(name):
    query = iroha.query('GetAccountDetail', account_id=name)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    response = net.send_query(query)
    data = response.account_detail_response
    return data
