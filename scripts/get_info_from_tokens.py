from .basics import *

data_append_frequency = 100
etherscan_frequency = 5 # per sec
with open('./build/interfaces/IERC20.json') as json_file:
    token_abi = json.load(json_file)['abi']

def main():
	# tokens loaded from etherscan
	already_loaded = load_file(tokens_stores_path)
	loaded_tokens = already_loaded.keys()
	old_len = len(loaded_tokens)
	print('Previously loaded tokens: {}'.format(old_len))


	# tokens stored now
	stored = load_file(pairs_info_path)
	tokens0 = [v['token0'] for k,v in stored.items()]
	tokens1 = [v['token1'] for k,v in stored.items()]
	tokens = set(tokens0+tokens1)
	new_len = len(tokens)
	print('Tokens available: {}'.format(new_len))

	# identify what to load
	tokens_to_load = list(set(tokens) - set(loaded_tokens))
	if len(tokens_to_load) == 0:
		print('No new pairs to load')
		return None
	else:
		print('Pairs loading: {} elements'.format(len(tokens_to_load)))


	# load new elements and append storage data
	new_loads = {}
	for num in range(len(tokens_to_load)):
		token_addr = tokens_to_load[num]

		try: 
			token = w3_parser.eth.contract(address=token_addr,abi=token_abi)
			new_loads[token_addr] = {}
			new_loads[token_addr]['symbol'] = token.functions.symbol().call()
			new_loads[token_addr]['decimals'] = token.functions.decimals().call()
			for k,v in etherscan_request(token_addr,ETHERSCAN_KEY).items():
				new_loads[token_addr][k] = v
		except:
			print ('problem with {}'.format(token_addr))
			continue

		time.sleep(1/etherscan_frequency)
		print(num/data_append_frequency)
		if num % data_append_frequency == 0 or num+1 == len(tokens_to_load): 
			append_file(tokens_stores_path, new_loads)
			print('{} elements appended'.format(len(new_loads.keys())))
			new_loads = {}
	return None



