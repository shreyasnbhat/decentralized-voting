from flask import render_template, request, redirect, url_for
from app import *

def bytes32_to_string(x):
    output = x.hex().rstrip("0")
    if len(output) % 2 != 0:
        output = output + '0'
    output = bytes.fromhex(output).decode('utf8')
    return output

@app.route('/', defaults = {'account_no':None}, methods = ['GET','POST'])
@app.route('/account/set/<string:account_no>', methods = ['POST'])
def homepage(account_no):
    if request.method == 'GET':
        accounts = server.eth.accounts

        return render_template('homepage.html', accounts = accounts)
    elif request.method == 'POST':
        session['account'] = account_no
        print(session['account'])
        return redirect(url_for('vote'))

@app.route('/vote',methods = ['GET','POST'])
def vote():
    if request.method == 'GET':
        voter_contract = server.eth.contract(address=CONTRACT_ADDRESS,
                                         abi=CONTRACT_ABI)
        candidates = [bytes32_to_string(i) for i in voter_contract.call().getCandidates()]
        return render_template('voter.html', candidates = candidates)

@app.route('/send_vote/<string:candidate>',methods = ['GET'])
def send_vote(candidate):
    if request.method == 'GET':
        voter_contract = server.eth.contract(address=CONTRACT_ADDRESS,
                                         abi=CONTRACT_ABI)
        tx_hash = voter_contract.functions.voteForCandidate(candidate.encode('utf-8')).transact({'from': DEFAULT_ACCOUNT})
        accounts = server.eth.accounts
        return redirect(url_for('homepage'))
