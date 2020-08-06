from flask import Flask, request
from flask_restful import Resource, Api
import irohaSDK
import irohaBUY
import binascii
import os
from iroha import IrohaCrypto

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


class ValidateUser(Resource):
    def post(self):
        print(request.form)
        name = request.form['Name']+'@mchain'
        private_key = request.form['priv_key']
        global priv_key
        priv_key =  private_key.encode()
        D = irohaSDK.get_userone_details(name)
        if D.detail:
            return {'user':'exist'}
        else:
            return {'user': 'Not exist'}


class CreateUser(Resource):
    def post(self):
        signin_name = request.form['SigninName']
        priva_key = binascii.b2a_hex(os.urandom(32))
        public_key = IrohaCrypto.derive_public_key(priv_key)
        D = irohaSDK.create_account(signin_name,public_key)
        return {'priv_key': priva_key.decode("utf-8")}


class GetBalance(Resource):
    def post(self):
        acc_name = request.form['acc_name']
        bal = irohaSDK.get_account_assets(acc_name)
        if bal:
            for asset in bal:
                balance = asset.balance
            return {'ans': balance}
        else:
            return {'ans': 0 }


class GetLabels(Resource):
    def get(self):
        assets = irohaSDK.get_account_assets('admin')
        Data = []
        for asset in assets:
            Data.append(asset.asset_id)
        return Data


class BuyMusic(Resource):
    def post(self):
        d = irohaBUY.instantiate(request.form['src'], request.form['dest'], request.form['amt'], priv_key)
        return {'bought': "success"}


class QueryAccount(Resource):
    def get(self):
        assets = irohaSDK.get_account_assets(request.form['acc_id'])
        Data = []
        for asset in assets:
            Data.append(asset.asset_id)
        return Data


class QueryMusic(Resource):
    def get(self):
        d = irohaSDK.get_asset_transaction(request.form['acc_id'], request.form['asset'])
        ans = []
        for i in d:
            for j in i.payload.reduced_payload.commands:
                ans.append(str(j.transfer_asset))
        return ans


class UploadMusic(Resource):
    def post(self):
        d = irohaBUY.createAsset(request.form['asset'],'test',0,priv_key,request.form['acc_name'])
        return {'upload': 'finished'}


class BuyCoin(Resource):
    def post(self):
        d = irohaSDK.transfer_coin_from_admin_to_user(request.form['acc_name'],request.form['amt'])
        return {'Bought': "successful"}


api.add_resource(ValidateUser, '/ValidateUser/')
api.add_resource(CreateUser, '/CreateUser/')
api.add_resource(GetBalance, '/GetBalance/')
api.add_resource(GetLabels, '/GetLabels/')
api.add_resource(BuyMusic, '/BuyMusic/')
api.add_resource(QueryAccount, '/QueryAccount/')
api.add_resource(QueryMusic, '/QueryMusic/')
api.add_resource(UploadMusic, '/UploadMusic/')
api.add_resource(BuyCoin, '/BuyCoin/')

