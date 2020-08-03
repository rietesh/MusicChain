import os
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc

import sys

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '0.0.0.0')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

user_private_key = IrohaCrypto.private_key()
user_public_key = IrohaCrypto.derive_public_key(user_private_key)
iroha = Iroha('admin@test')
net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))


def create_domain_and_asset():
    commands = [
        iroha.command('CreateDomain', domain_id='domain', default_role='user'),
        iroha.command('CreateAsset', asset_name='coin',
                      domain_id='domain', precision=2)
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


def add_coin_to_admin():
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id='coin#domain', amount='1000.00')
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


def create_account(signin_name,pub_key):
    tx = iroha.transaction([
        iroha.command('CreateAccount', account_name=signin_name, domain_id='test',
                      public_key=pub_key)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    net.send_tx(tx)


def transfer_coin_from_admin_to_user(acc_id,amt):
    tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id='admin@test', dest_account_id=acc_id+'@test',
                      asset_id='coin#test', amount=amt)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    net.send_tx(tx)


def get_account_assets(acc_name):
    """
    List all the assets of userone@domain
    """
    acc_id = acc_name + '@test'
    query = iroha.query('GetAccountAssets', account_id=acc_id)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

    response = net.send_query(query)
    data = response.account_assets_response.account_assets

    return data


def get_asset_transaction(acc_id,asset):
    query = iroha.query('GetAccountAssetTransactions', account_id= acc_id+'@test', asset_id=asset+'#test', page_size= 5)
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
