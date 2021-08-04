#from .basics import *
import pickle

def load_file(path):
    with open(path, 'rb') as file:
        loaded = pickle.load(file)
    return loaded

def append_file(path,new_content:dict):
    before = load_file(path)
    after = before
    for k,v in new_content.items():
        after[k] = v
    with open(path, 'wb') as file:
        pickle.dump(after, file)


stablecoins = {
	'0x956F47F50A910163D8BF957Cf5846D573E7f87CA': 18,
	'0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48': 6,
	'0xdAC17F958D2ee523a2206206994597C13D831ec7': 6,
	'0xa47c8bf37f92aBed4A126BDA807A7b7498661acD': 18,
	'0x6B175474E89094C44Da98b954EedeAC495271d0F': 18,
	'0x853d955aCEf822Db058eb8505911ED77F175b99e': 18,
	'0xD46bA6D942050d489DBd938a2C909A5d5039A161': 9
}

pairs_info_path = r'C:\_MAIN\cryptodev\hypotheses\uniswap_tokens\data/pair_info_dict'
tokens_stores_path = r'C:\_MAIN\cryptodev\hypotheses\uniswap_tokens\data/tokens_dict'


pairs = load_file(pairs_info_path)
tokens0 = [v['token0'] for k,v in pairs.items()]
tokens1 = [v['token1'] for k,v in pairs.items()]
tokens = set(tokens0+tokens1)

traded_to_stable = {}
for k,v in pairs.items():

	if v['token1'] in stablecoins.keys() and v['token0'] not in stablecoins.keys():
		t = v['token0']
		s = v['token1']
		price = 0 if v['reserve0'] == 0 else v['reserve1']/(10**stablecoins[s]) / v['reserve0']
		traded_to_stable[t] = price #if traded_to_stable[t] != None else (traded_to_stable[t] + price ) / 2

	if v['token0'] in stablecoins.keys() and v['token1'] not in stablecoins.keys():
		t = v['token1']
		s = v['token0']
		price = 0 if v['reserve0'] == 0 else v['reserve0']/(10**stablecoins[s]) / v['reserve1']
		traded_to_stable[t] = price #if traded_to_stable[t] != None else (traded_to_stable[t] + price ) / 2

traded_to_valuable = {}
for k,v in pairs.items():
	

	if v['token1'] in traded_to_stable.keys() and v['token0'] not in traded_to_stable.keys():
		t = v['token0']
		s = v['token1']
		if t == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
			print('boom')
		price = 0 if v['reserve0'] == 0 else v['reserve1'] * traded_to_stable[s] / v['reserve0']
		traded_to_valuable[t] = price

	if v['token0'] in traded_to_stable.keys() and v['token1'] not in traded_to_stable.keys():
		t = v['token1']
		s = v['token0']
		if t == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
			print(s,k)
		price = 0 if v['reserve1'] == 0 else v['reserve0'] * traded_to_stable[s] / v['reserve1']
		traded_to_valuable[t] = price	

all_valued = traded_to_stable
for k,v in traded_to_valuable.items():
	all_valued[k] = v

print(len(all_valued))

pair_valuation = {}
for k,v in pairs.items():
	if v['token0'] in all_valued.keys():
		r = v['reserve0'] * all_valued[v['token0']]
	elif v['token1'] in all_valued.keys():
		r = v['reserve1'] * all_valued[v['token1']]
	else:
		r = 0
	pair_valuation[k] = int(r *2)

for k,v in pair_valuation.items():
	print(k, v)





