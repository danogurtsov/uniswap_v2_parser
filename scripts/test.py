import requests, json
ETHERSCAN_KEY = 'VZCZV8C7SJ3T9SEA36QJVT8E2EYNXJY1QZ'

def etherscan_request(contract_address):
    api_return = requests.get('https://api.etherscan.io/api?module=contract&action=getsourcecode&address={}&apikey={}'.format(
        contract_address,ETHERSCAN_KEY))
    if not api_return.status_code == 200: raise Exception('Etherscan API request failed')
    result = json.loads(api_return.text)['result'][0]
    return result

