import os
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc


IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '10.148.0.8')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@mchain')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', '505e3ee6da65ad07268236e49a302d982c027e353ee9bd0acb89b2c395151deb')


def instantiate(src,dest,amt,priv_key):
    iroha = Iroha(src+'@mchain')
    net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))
    tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id=src+'@mchain', dest_account_id=dest+'@mchain',
                      asset_id='coin#mchain', amount=amt)
    ])
    priv = priv_key
    IrohaCrypto.sign_transaction(tx, priv)
    net.send_tx(tx)


def createAsset(asset_name,domain_id,precision,priv_key,name):
    iroha = Iroha(name + '@mchain')
    net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))
    tx = iroha.transaction([
        iroha.command('CreateAsset', asset_name=asset_name, domain_id=domain_id, precision=precision)])
    IrohaCrypto.sign_transaction(tx, priv_key)
    net.send_tx(tx)
