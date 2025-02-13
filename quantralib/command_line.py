import argparse
from .cleos import Cleos
from .testeos import TestEos
from .utils import parse_key_file
from .exceptions import InvalidPermissionFormat, EOSSetSameAbi, EOSSetSameCode
import json


def console_print(data):
    print(json.dumps(data, indent=4))


def set_abi(ce, account, permission, abi, key, broadcast, timeout):
    print('setting abi file {}'.format(abi))
    try:
        console_print(ce.set_abi(account, permission, abi, key, broadcast=broadcast, timeout=timeout))
    except EOSSetSameAbi:
        print('Skipping set abi because the new abi is the same as the existing abi')


def set_code(ce, account, permission, code, key, broadcast, timeout):
    print('setting code file {}'.format(code))
    try:
        console_print(ce.set_code(account, permission, code, key, broadcast=broadcast, timeout=timeout))
    except EOSSetSameCode:
        print('Skipping set code because the new code is the same as the existing code')


def cleos():
    parser = argparse.ArgumentParser(description='Command Line Interface to EOSIO via python')
    parser.add_argument('--api-version', '-v', type=str, default='v1', action='store', dest='api_version')
    parser.add_argument('--url', '-u', type=str, action='store', default='https://proxy.eosnode.tools', dest='url')
    parser.add_argument('--time-out', type=int, action='store', default=30, dest='timeout')
    subparsers = parser.add_subparsers(dest='subparser')
    # get
    get_parser = subparsers.add_parser('get')
    get_subparsers = get_parser.add_subparsers(dest='get')
    # info
    get_subparsers.add_parser('info')
    # block
    block_parser = get_subparsers.add_parser('block')
    #block_parser.add_argument('block', type=str)
    block_parser.add_argument('--block', '-b', type=str, action='store', required=True, dest='block')
    # account
    account_parser = get_subparsers.add_parser('account')
    account_parser.add_argument('--account', '-a', type=str, action='store', required=True, dest='account')
    #account_parser.add_argument('account', type=str)
    # code
    code_parser = get_subparsers.add_parser('code')
    code_parser.add_argument('--account', '-a', type=str, action='store', required=True, dest='account')
    #code_parser.add_argument('account', type=str)
    # abi
    abi_parser = get_subparsers.add_parser('abi')
    abi_parser.add_argument('--account', '-a', type=str, action='store', required=True, dest='account')
    abi_parser.add_argument('--raw', action='store_true', dest='raw')
    #abi_parser.add_argument('account', type=str)
    # table
    table_parser = get_subparsers.add_parser('table')
    table_parser.add_argument('--code', '-c', type=str, action='store', required=True, dest='code')
    table_parser.add_argument('--scope', '-S', type=str, action='store', required=True, dest='scope')
    table_parser.add_argument('--table', '-t', type=str, action='store', required=True, dest='table')
    #table_parser.add_argument('contract', type=str, help='The contract who owns the table (required)')
    #table_parser.add_argument('scope', type=str, help='The scope within the contract in which the table is found (required)')
    # table_parser.add_argu`ment('table', type=str, help='The name of the table as specified by the contract abi (required)')
    table_parser.add_argument('--index', type=int, action='store', default=1, dest='index_position', help='Index number')
    table_parser.add_argument('--key-type', type=str, action='store', default="i64", dest='key_type', help='The key type of --index')
    table_parser.add_argument('--lower-bound', type=str, action='store', default=0, dest='lower_bound', help='The name of the key to index by as defined by the abi, defaults to primary key')
    table_parser.add_argument('--upper-bound', type=str, action='store', default=-1, dest='upper_bound')
    table_parser.add_argument('--limit', type=int, action='store', default=1000, dest='limit')
    # currency
    currency = get_subparsers.add_parser('currency')
    currency.add_argument('type', choices=['balance', 'stats'], type=str)
    currency.add_argument('--code', '-c', type=str, action='store', required=True, dest='code')
    currency.add_argument('--symbol', '-s', type=str, action='store', required=True, dest='symbol')
    currency.add_argument('--account', '-a', type=str, action='store', dest='account')
    # accounts
    accounts = get_subparsers.add_parser('accounts')
    accounts.add_argument('--key', '-k', type=str, action='store', required=True, dest='key')
    # transaction
    transaction = get_subparsers.add_parser('transaction')
    transaction.add_argument('--transaction', '-t', type=str, action='store', required=True, dest='transaction')
    # actions
    actions = get_subparsers.add_parser('actions')
    actions.add_argument('--account', '-a', type=str, action='store', required=True, dest='account')
    actions.add_argument('--pos', type=int, action='store', default=-1, dest='pos')
    actions.add_argument('--offset', type=int, action='store', default=-20, dest='offset')
    # bin2json
    bin_json = get_subparsers.add_parser('bin2json')
    bin_json.add_argument('--code', '-c', type=str, action='store', required=True, dest='code')
    bin_json.add_argument('--action', '-a', type=str, action='store', required=True, dest='action')
    bin_json.add_argument('--binargs', '-b', type=str, action='store', required=True, dest='binargs')
    # json2bin
    # create
    create_parser = subparsers.add_parser('create')
    create_subparsers = create_parser.add_subparsers(dest='create')
    # create EOS key
    create_key = create_subparsers.add_parser('key')
    group_key = create_key.add_mutually_exclusive_group(required=True)
    group_key.add_argument('--key-file', '-k', type=str, action='store', help='file to output the keys too', dest='key_file')
    group_key.add_argument('--to-console', '-c', action='store_true', help='output to the console', dest='to_console')
    # push
    push_parser = subparsers.add_parser('push')
    push_subparsers = push_parser.add_subparsers(dest='push')
    push_action = push_subparsers.add_parser('action')
    push_action.add_argument('account', type=str, action='store', help='account name for the contract to execute')
    push_action.add_argument('action', type=str, action='store', help='action to execute')
    push_action.add_argument('data', type=str, action='store', help='JSON string of the arguments to the contract action')
    push_action.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')
    push_action.add_argument('--permission', '-p', type=str, action='store', required=True, help='account and permission level to use, e.g \'account@permission\'', dest='permission')
    push_action.add_argument('--dont-broadcast', '-d', action='store_false', default=True, help='do not broadcast the transaction to the network.', dest='broadcast')
    # multisig
    msig_parser = subparsers.add_parser('multisig')
    msig_subparsers = msig_parser.add_subparsers(dest='multisig')
    msig_review = msig_subparsers.add_parser('review')
    msig_review.add_argument('proposer', type=str, action='store', help='proposer name')
    msig_review.add_argument('proposal', type=str, action='store', help='proposal name')
    # system commands
    # listproducers
    system_parser = subparsers.add_parser('system')
    system_subparsers = system_parser.add_subparsers(dest='system', help='Send eosio.system contract action to the blockchain')
    producer_sys = system_subparsers.add_parser('listproducers')
    producer_sys.add_argument('--lower-bound', type=str, action='store', default="", dest='lower_bound')
    producer_sys.add_argument('--limit', type=int, action='store', default=50, dest='limit')
    # new account
    newacct_parser = system_subparsers.add_parser('newaccount', help='create a new account')
    newacct_parser.add_argument('creator', type=str, action='store')
    newacct_parser.add_argument('creator_key', type=str, action='store')
    newacct_parser.add_argument('account', type=str, action='store')
    newacct_parser.add_argument('owner', type=str, action='store')
    newacct_parser.add_argument('--active', '-a', type=str, action='store', dest='active')
    newacct_parser.add_argument('--stake-net', type=str, action='store', default='1.0000 EOS', dest='stake_net')
    newacct_parser.add_argument('--stake-cpu', type=str, action='store', default='1.0000 EOS', dest='stake_cpu')
    newacct_parser.add_argument('--buy-ram-kbytes', type=int, action='store', default=8, dest='ramkb')
    newacct_parser.add_argument('--permission', '-p', type=str, action='store', default='active', dest='permission')
    newacct_parser.add_argument('--transfer', action='store_true', default=False, dest='transfer')
    newacct_parser.add_argument('--dont-broadcast', '-d', action='store_false', default=True, dest='broadcast')
    # set
    set_parser = subparsers.add_parser('set')
    set_subparsers = set_parser.add_subparsers(dest='set', help='Set or update blockchain state')
    # abi
    set_abi_parser = set_subparsers.add_parser('abi')
    set_abi_parser.add_argument('account', type=str, action='store', help='The account to set code for')
    set_abi_parser.add_argument('abi', type=str, action='store', help='The fullpath containing the contract abi')
    set_abi_parser.add_argument('key', type=str, action='store', help='Key to sign ')
    set_abi_parser.add_argument('--permission', '-p', type=str, action='store', default='active', dest='permission')
    set_abi_parser.add_argument('--dont-broadcast', '-d', action='store_false', default=True, dest='broadcast')
    # code
    set_code_parser = set_subparsers.add_parser('code')
    set_code_parser.add_argument('account', type=str, action='store', help='The account to set abi for')
    set_code_parser.add_argument('code', type=str, action='store', help='The fullpath containing the contract code')
    set_code_parser.add_argument('key', type=str, action='store', help='Key to sign the transaction')
    set_code_parser.add_argument('--permission', '-p', type=str, action='store', default='active', dest='permission')
    set_code_parser.add_argument('--dont-broadcast', '-d', action='store_false', default=True, dest='broadcast')
    # contract
    set_contract_parser = set_subparsers.add_parser('contract')
    set_contract_parser.add_argument('account', type=str, action='store', help='The account to set abi for')
    set_contract_parser.add_argument('code', type=str, action='store', help='The fullpath containing the contract code')
    set_contract_parser.add_argument('abi', type=str, action='store', help='The fullpath containing the contract abo')
    set_contract_parser.add_argument('key', type=str, action='store', help='Key to sign the transaction')
    set_contract_parser.add_argument('--permission', '-p', type=str, action='store', default='active', dest='permission')
    set_contract_parser.add_argument('--dont-broadcast', '-d', action='store_false', default=True, dest='broadcast')
    # random commands
    random_parser = subparsers.add_parser('random')
    random_parser.add_argument('--contract_account', '-c', type=str, action='store', help='account with QRandom contract', default="quant.random")
    random_parser.add_argument('--tokens_account', '-t', type=str, action='store', help='account with tokens to operate within QRandom contract', default="eosio.token")
    random_subparsers = random_parser.add_subparsers(dest='random', help='Send (q)random action to the blockchain')
    # getconfig
    getconfig_random = random_subparsers.add_parser('getconfig')
    # getrandom
    getrandom_random = random_subparsers.add_parser('getrandom')
    getrandom_random.add_argument('account', type=str, action='store', help='account name to buy a random value for')
    # buyrandom
    buy_random = random_subparsers.add_parser('buyrandom')
    buy_random.add_argument('account', type=str, action='store', help='account name to buy a random value for')
    buy_random.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')

    # process args
    args = parser.parse_args()
    #
    # connect
    ce = Cleos(url=args.url, version=args.api_version)

    # run commands based on subparser
    # GET
    if args.subparser == 'get':
        if args.get == 'info':
            console_print(ce.get_info(timeout=args.timeout))
        elif args.get == 'block':
            console_print(ce.get_block(args.block, timeout=args.timeout))
        elif args.get == 'account':
            console_print(ce.get_account(args.account, timeout=args.timeout))
        elif args.get == 'code':
            console_print(ce.get_code(args.account, timeout=args.timeout))
        elif args.get == 'abi':
            if args.raw:
                console_print(ce.get_raw_abi(args.account, timeout=args.timeout))
            else:
                console_print(ce.get_abi(args.account, timeout=args.timeout))
        elif args.get == 'table':
            console_print(ce.get_table(code=args.code,
                                       scope=args.scope,
                                       table=args.table,
                                       index_position=args.index_position,
                                       key_type=args.key_type,
                                       lower_bound=args.lower_bound,
                                       upper_bound=args.upper_bound,
                                       limit=args.limit,
                                       timeout=args.timeout))

        elif args.get == 'currency':
            if args.type == 'balance':
                if args.account:
                    console_print(ce.get_currency_balance(args.account, code=args.code, symbol=args.symbol, timeout=args.timeout))
                else:
                    raise ValueError('--account is required')
            else:
                console_print(ce.get_currency(code=args.code, symbol=args.symbol, timeout=args.timeout))
        elif args.get == 'accounts':
            console_print(ce.get_accounts(args.key, timeout=args.timeout))
        elif args.get == 'transaction':
            console_print(ce.get_transaction(args.transaction, timeout=args.timeout))
        elif args.get == 'actions':
            console_print(ce.get_actions(args.account, pos=args.pos, offset=args.offset, timeout=args.timeout))
        elif args.get == 'bin2json':
            console_print(ce.abi_bin_to_json(args.code, args.action, args.binargs, timeout=args.timeout))
    # PUSH
    elif args.subparser == 'push':
        if args.push == 'action':
            priv_key = parse_key_file(args.key_file)
            arguments = json.loads(args.data)
            try:
                account, permission = args.permission.split('@')
            except ValueError:
                raise InvalidPermissionFormat('Permission format needs to be account@permission')
            payload = {
                "account": args.account,
                "name": args.action,
                "authorization": [{
                    "actor": account,
                    "permission": permission,
                }],
            }
            data = ce.abi_json_to_bin(args.account, args.action, arguments)
            print(data)
            payload['data'] = data['binargs']
            print(payload)
            trx = {"actions": [payload]}
            resp = ce.push_transaction(trx, priv_key, broadcast=args.broadcast)
            console_print(resp)
    # MULISIG
    elif args.subparser == "multisig":
        if args.multisig == "review":
            console_print(ce.multisig_review(args.proposer, args.proposal))
    # CREATE
    elif args.subparser == 'create':
        if args.create == 'key':
            k = ce.create_key()
            priv_key = 'Private key: {}'.format(k.to_wif())
            pub_key = 'Public key: {}'.format(k.to_public())
            if args.to_console:
                print(priv_key)
                print(pub_key)
            else:
                with open(args.key_file, 'w') as wf:
                    wf.write(priv_key + '\n')
                    wf.write(pub_key + '\n')
                print("Wrote keys to {}".format(args.key_file))
    # SET
    elif args.subparser == 'set':
        if args.set == 'abi':
            set_abi(ce, args.account, args.permission, args.abi, args.key, broadcast=args.broadcast, timeout=args.timeout)
        elif args.set == 'code':
            set_code(ce, args.account, args.permission, args.code, args.key, broadcast=args.broadcast, timeout=args.timeout)
            pass
        elif args.set == 'contract':
            set_abi(ce, args.account, args.permission, args.abi, args.key, broadcast=args.broadcast, timeout=args.timeout)
            set_code(ce, args.account, args.permission, args.code, args.key, broadcast=args.broadcast, timeout=args.timeout)
            pass
    # SYSTEM
    elif args.subparser == 'system':
        if args.system == 'newaccount':
            resp = ce.create_account(args.creator, args.creator_key, args.account, args.owner, args.active,
                                     stake_net=args.stake_net, stake_cpu=args.stake_cpu, ramkb=args.ramkb,
                                     permission=args.permission, transfer=args.transfer, broadcast=args.transfer,
                                     timeout=args.timeout)
            console_print(resp)
        elif args.system == 'listproducers':
            resp = ce.get_producers(lower_bound=args.lower_bound, limit=args.limit)
            console_print(resp)
    elif args.subparser == 'random':
        from .erandom import EOSRandom
        if args.random == 'buyrandom':
            priv_key = parse_key_file(args.key_file)
        else:
            from .cipher import generate_dynamic_key
            priv_key = generate_dynamic_key()

        chain = EOSRandom(args.contract_account,
                          p_key=priv_key,
                          tokens_account=args.tokens_account,
                          chain_url=args.url)
        if args.random == 'getconfig':
            console_print(chain.get_config_table())
        if args.random == 'getrandom':
            console_print(chain.get_randresult(account=args.account))
        if args.random == 'buyrandom':
            console_print(chain.buy_random(account=args.account))

def testeos():
    parser = argparse.ArgumentParser(description='EOSIO testing harness')
    parser.add_argument('--yaml', '-y', type=str, action='store', required=True, dest='yaml_loc')
    parser.add_argument('--tests', '-t', nargs='*', action='store', default="all", dest='tests')
    # process args
    args = parser.parse_args()

    tester = TestEos(args.yaml_loc)
    if args.tests == 'all':
        tester.run_test_all()
    else:
        for test in args.tests:
            tester.run_test_one(test)
