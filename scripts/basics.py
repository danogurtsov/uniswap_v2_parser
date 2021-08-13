from brownie import *
from .reports import *
import pickle, json, requests, time
from web3 import Web3


pairs_stores_path = './data/pair_addresses_dict'
pairs_info_path = './data/pair_info_dict'
tokens_stores_path = './data/tokens_dict'

ENDPOINT = 'https://mainnet.infura.io/v3/49e0071853c348d7aa0968e8a69b7fba'
ETHERSCAN_KEY = 'VZCZV8C7SJ3T9SEA36QJVT8E2EYNXJY1QZ'

data_append_frequency = 100
etherscan_frequency = 5 # per sec

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
    #   SourceCode
    #   ABI
    #   ContractName
    #   CompilerVersion
    #   OptimizationUsed
    #   Runs
    #   ConstructorArguments
    #   EVMVersion
    #   Library
    #   LicenseType
    #   Proxy
    #   Implementation
    #   SwarmSource
    api_return = requests.get('https://api.etherscan.io/api?module=contract&action=getsourcecode&address={}&apikey={}'.format(
        contract_address,ETHERSCAN_KEY))
    if not api_return.status_code == 200: raise Exception('Etherscan API request failed')
    result = json.loads(api_return.text)['result'][0]
    return result


# address => decimals
stablecoins = {
    '0x956F47F50A910163D8BF957Cf5846D573E7f87CA': 18,
    '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48': 6,
    '0xdAC17F958D2ee523a2206206994597C13D831ec7': 6,
    '0xa47c8bf37f92aBed4A126BDA807A7b7498661acD': 18,
    '0x6B175474E89094C44Da98b954EedeAC495271d0F': 18,
    '0x853d955aCEf822Db058eb8505911ED77F175b99e': 18,
    '0xD46bA6D942050d489DBd938a2C909A5d5039A161': 9
}