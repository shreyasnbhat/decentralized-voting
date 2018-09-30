from flask import render_template, request, flash, redirect, url_for
from app import *
import os

CONTRACT_ADDRESS = None
CONTRACT_ABI = None

valid_contract_addresses = []


def deploy_contract():
    global CONTRACT_ABI, CONTRACT_ADDRESS

    os.chdir('../../')
    print(os.path.abspath(os.curdir))
    os.system('./compile.sh > /dev/null')

    with open('build/contracts/VotingContract.json') as f:
        voter_contract_data = json.load(f)

    with open('dump.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    CONTRACT_ADDRESS = server.toChecksumAddress(content[12].split(': ')[1].strip())

    valid_contract_addresses.append(CONTRACT_ADDRESS)

    CONTRACT_ABI = voter_contract_data['abi']

    session['abi'] = CONTRACT_ABI
    session['contract_address'] = CONTRACT_ADDRESS

    os.chdir('flask/organization')


def bytes32_to_string(x):
    output = x.hex().rstrip("0")
    if len(output) % 2 != 0:
        output = output + '0'
    output = bytes.fromhex(output).decode('utf8')
    return output


def add_voter(address, id):
    voter_contract = server.eth.contract(address=CONTRACT_ADDRESS,
                                         abi=CONTRACT_ABI)
    account = session.get('account', DEFAULT_ACCOUNT)
    tx_hash = voter_contract.functions.addVoter(address).transact({'from': account})
    receipt = server.eth.waitForTransactionReceipt(tx_hash)
    print("Added", address)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        print(valid_contract_addresses)
        if len(valid_contract_addresses) == 0:
            return render_template('homepage.html')
        else:
            return render_template("homepage.html", deployed=True, address=CONTRACT_ADDRESS)
    else:
        deploy_contract()
        return render_template("homepage.html", deployed=True, address=CONTRACT_ADDRESS)


@app.route('/add/voter/', methods=['POST'])
def add_voter_endpoint():
    print(request.form)
    address = request.form['address']
    id = request.form['id']
    add_voter(address, id)
    return redirect(url_for('homepage'))


@app.route('/choose', defaults={'account_no': None}, methods=['GET', 'POST'])
@app.route('/account/set/<string:account_no>', methods=['POST'])
def choose_account(account_no):
    if request.method == 'GET':
        accounts = [server.toChecksumAddress(i) for i in server.eth.accounts]
        return render_template('account.html', accounts=accounts)
    elif request.method == 'POST':
        session['account'] = account_no
        return redirect(url_for('homepage'))
