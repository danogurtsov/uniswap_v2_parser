from .basics import *

data_append_frequency = 100
with open('./build/interfaces/UniswapV2Pair.json') as json_file:
    unipair_abi = json.load(json_file)['abi']

def main():
    # check already loaded pairs
    already_loaded = load_file(pairs_info_path)
    loaded_pairs = already_loaded.keys()
    old_len = len(loaded_pairs)
    print('Previously loaded pairs: {}'.format(old_len))

    # check pairs length
    pairs = load_file(pairs_stores_path)
    new_len = len(pairs.values())
    print('Pairs available: {}'.format(new_len))

    # identify what to load
    pairs_to_load = list(set(pairs.values()) - set(loaded_pairs))
    if len(pairs_to_load) == 0:
        print('No new pairs to load')
        return None
    else:
        print('Pairs loading: {} elements'.format(len(pairs_to_load)))

    # load new elements and append storage data
    new_loads = {}
    for num in range(len(pairs_to_load)):
        pair_addr = pairs_to_load[num]

        try: 
            pair = w3_parser.eth.contract(address=pair_addr,abi=unipair_abi)
        except:
            print ('problem with {}'.format(pair_addr))
            continue

        new_loads[pair_addr] = {}
        new_loads[pair_addr]['reserve0'] = pair.functions.getReserves().call()[0]
        new_loads[pair_addr]['reserve1'] = pair.functions.getReserves().call()[1]
        new_loads[pair_addr]['token0']   = pair.functions.token0().call()
        new_loads[pair_addr]['token1']   = pair.functions.token1().call()
        print(num/data_append_frequency)

        if num % data_append_frequency == 0 or num+1 == len(pairs_to_load): 
            append_file(pairs_info_path, new_loads)
            print('{} elements appended'.format(len(new_loads.keys())))
            new_loads = {}
    return None