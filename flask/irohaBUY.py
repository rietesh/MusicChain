import os
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc


IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '0.0.0.0')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')


def instantiate(src,dest,amt,priv_key):
    iroha = Iroha(src+'@test')
    net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))
    tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id=src+'@test', dest_account_id=dest+'@test',
                      asset_id='coin#test', amount=amt)
    ])
    priv = priv_key
    IrohaCrypto.sign_transaction(tx, priv)
    net.send_tx(tx)


def createAsset(asset_name,domain_id,precision,priv_key,name):
    iroha = Iroha(name + '@test')
    net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))
    tx = iroha.transaction([
        iroha.command('CreateAsset', asset_name=asset_name, domain_id=domain_id, precision=precision)])
    IrohaCrypto.sign_transaction(tx, priv_key)
    net.send_tx(tx)
