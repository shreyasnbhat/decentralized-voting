from flask import render_template, request, flash, redirect, url_for
from app import *


def bytes32_to_string(x):
    output = x.hex().rstrip("0")
    if len(output) % 2 != 0:
        output = output + '0'
    output = bytes.fromhex(output).decode('utf8')
    return output


@app.route('/', defaults={'account_no': None}, methods=['GET', 'POST'])
@app.route('/account/set/<string:account_no>', methods=['POST'])
def homepage(account_no):
    if request.method == 'GET':
        accounts = [server.toChecksumAddress(i) for i in server.eth.accounts]
        return render_template('homepage.html', accounts=accounts)
    elif request.method == 'POST':
        session['account'] = account_no
        return redirect(url_for('vote'))


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'GET':
        voter_contract = server.eth.contract(address=CONTRACT_ADDRESS,
                                             abi=CONTRACT_ABI)
        candidates = [bytes32_to_string(i) for i in voter_contract.call().getCandidates()]
        votes = []
        for i in candidates:
            votes_for_candidate = voter_contract.functions.totalVotesFor(i.encode('utf-8')).call()
            votes.append(votes_for_candidate)
        return render_template('voter.html', candidates=candidates, votes=votes)


@app.route('/send_vote/<string:candidate>', methods=['POST'])
def send_vote(candidate):
    if request.method == 'POST':
        voter_contract = server.eth.contract(address=CONTRACT_ADDRESS,
                                             abi=CONTRACT_ABI)
        try:
            account = session.get('account', DEFAULT_ACCOUNT)
            if account is not None:
                tx_hash = voter_contract.functions.voteForCandidate(candidate.encode('utf-8')).transact(
                    {'from': account})
                receipt = server.eth.waitForTransactionReceipt(tx_hash)
                print("Gas Used ", receipt.gasUsed)
            else:
                flash('No account was chosen')
        except ValueError:
            flash('Vote Limit Exceed or Voter not registered by Authority')

        return redirect(url_for('vote'))
