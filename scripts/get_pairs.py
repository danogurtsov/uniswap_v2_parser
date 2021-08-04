from .basics import *

data_append_frequency = 200 # elements

def main():
    # check already loaded pairs
    already_loaded = load_file(pairs_stores_path)
    loaded_nums = already_loaded.keys()
    old_len = len(loaded_nums)
    print('Previously loaded pairs: {}'.format(old_len))

    # check pairs length
    addr_factory = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
    factory = interface.UniswapV2Factory(addr_factory)
    w3_factory = w3_parser.eth.contract(address=addr_factory,abi=factory.abi)
    new_len = w3_factory.functions.allPairsLength().call()
    print('Pairs found in factory: {}'.format(new_len))

    # identify what to load
    pairs_to_load = list(set(range (new_len)) - set(loaded_nums))
    if len(pairs_to_load) == 0:
        print('No new tokens to load')
        return None
    else:
        print('Pairs loading: from {} to {} with {} elements'.format(min(pairs_to_load),max(pairs_to_load),len(pairs_to_load)))

    # load new elements and append storage data
    new_loads = {}
    for num in range(len(pairs_to_load)):
        pairnum = pairs_to_load[num]
        pair_addr = w3_factory.functions.allPairs(pairnum).call()
        new_loads[pairnum] = pair_addr
        if num % data_append_frequency == 0 or num+1 == len(pairs_to_load): 
            append_file(pairs_stores_path, new_loads)
            print('{} elements appended'.format(len(new_loads.keys())))
            new_loads = {}
    return None





