from flask import Flask, session
import web3
from web3 import Web3, HTTPProvider
import json
from flask_session import Session

# Flask App initialization
app = Flask(__name__)
app.secret_key = 'secret_key'

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

server = Web3(HTTPProvider('http://localhost:7545'))

CONTRACT_ADDRESS = "0xFd10018A62c8C84f82F5DA0F386DF9A2E7888ee6"
DEFAULT_ACCOUNT = "0xf847465aaC31C383540B56eb2B5a57f2C8192172"

with open('../build/contracts/VotingContract.json') as f:
    voter_contract_data = json.load(f)

CONTRACT_ABI = voter_contract_data['abi']

from app import views
