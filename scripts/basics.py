from brownie import *
from .reports import *
import pickle, json, requests, time
from web3 import Web3

pairs_stores_path = './data/pair_addresses_dict'
pairs_info_path = './data/pair_info_dict'
tokens_stores_path = './data/tokens_dict'

ENDPOINT = 'https://mainnet.infura.io/v3/49e0071853c348d7aa0968e8a69b7fba'
ETHERSCAN_KEY = 'VZCZV8C7SJ3T9SEA36QJVT8E2EYNXJY1QZ'


w3_parser = Web3(Web3.HTTPProvider(ENDPOINT))

BIGNUMBER = (10**18) 

def load_file(path):
    try:
        with open(path, 'rb') as file:
            loaded = pickle.load(file)
    except:
        loaded = {}
    return loaded

def append_file(path,new_content:dict):
    before = load_file(path)
    after = before
    for k,v in new_content.items():
        after[k] = v
    with open(path, 'wb') as file:
        pickle.dump(after, file)

def etherscan_request(contract_address,key):
    # returned keys:
    # SourceCode
    # ABI
    # ContractName
    # CompilerVersion
    # OptimizationUsed
    # Runs
    # ConstructorArguments
    # EVMVersion
    # Library
    # LicenseType
    # Proxy
    # Implementation
    # SwarmSource
    api_return = requests.get('https://api.etherscan.io/api?module=contract&action=getsourcecode&address={}&apikey={}'.format(
        contract_address,ETHERSCAN_KEY))
    if not api_return.status_code == 200: raise Exception('Etherscan API request failed')
    result = json.loads(api_return.text)['result'][0]
    return result