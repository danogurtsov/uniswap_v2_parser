# my custom lib to visualize balances when brownie is running

from beautifultable import BeautifulTable
from brownie import *

default_decimals = 18
network_currency = 'ETH'


class Report (object):
    def __init__(self):
        self.tokens = []
        self.accounts = []
        self.contracts = []
        self.default_account_names = {}
        for i in range(len(accounts)):
            acc_name = 'Account {} {}..'.format(str(i),accounts[i].address[:5])
            self.default_account_names[accounts[i]] = acc_name

    def add_token(self, _contract):
        assert type(_contract) is network.contract.ProjectContract, 'Report.add_token(): _contract argument is not <Contract>'
        try:
            _name = _contract.symbol()
        except:
            _name = _contract._name
        if _contract not in self.tokens: self.tokens.append((_contract,_name))

    def add_account(self, _account, _name='default'):
        assert type(_account) is network.account.Account, 'Report.add_account(): _account argument is not <Account>'
        if _name=='default': _name = self.default_account_names[_account]
        if _account not in self.accounts: self.accounts.append((_account,_name))

    def add_contract(self, _contract, _name='default'):
        assert type(_contract) is network.contract.ProjectContract, 'Report.add_contract(): _contract argument is not <Contract>'
        if _name=='default': _name = _contract._name + ' {}..'.format(_contract.address[:5])
        if _contract not in self.contracts: self.contracts.append((_contract, _name))


    def print(self):
        table = BeautifulTable()
        first_column = '...'

        # calculate balances
        addresses = []
        addresses.extend([x[0] for x in self.accounts])
        addresses.extend([x[0] for x in self.contracts])
        for address in addresses:
            #calculate eth balance
            clean_balances = []
            eth_balance = number_presentation(address.balance(),default_decimals)
            clean_balances.append(eth_balance)
            # calculate token balances
            for token in self.tokens:
                balance = token[0].balanceOf(address)
                try:
                    decimals = token[0].decimals()
                except:
                    decimals = default_decimals
                token_balance = number_presentation(balance,decimals)
                clean_balances.append(token_balance)
            table.rows.append(clean_balances)

        # add column names
        headers = [network_currency]
        headers.extend([token[1] for token in self.tokens])
        table.columns.header = headers

        # add row names
        cyan = '\033[1;36;40m'
        magenda = '\033[1;35;40m'
        accounts_color = cyan
        contracts_color = magenda
        rows = [colored(acc[1],accounts_color) for acc in self.accounts]
        rows.extend([colored(acc[1],contracts_color) for acc in self.contracts])
        table.columns.insert(0, rows, header=first_column)

        # some style
        table.columns.alignment = BeautifulTable.ALIGN_RIGHT
        table.columns.alignment[first_column] = BeautifulTable.ALIGN_LEFT
        table.set_style(BeautifulTable.STYLE_RST)

        print(table)
        print(' ')


    def txt_print(self, txt:str):
        color = '\033[33m'
        print(colored('---------------------------------',color))
        print(colored('   '+txt,color))
        print(colored('---------------------------------',color))

def colored(txt:str, colorcode):
    ENDC = '\033[0m'
    return colorcode + txt + ENDC

# allow readable presentation of numbers with many decimals
# from "10000000000" to "10 000 000 000"
# decimals in input will also show the transformation from BIGNUMBER
def number_presentation (num, decimals):
    num = str(int(num))
    if len(num) <= decimals:
        for i in range(decimals - len(num) + 1):
            num = '0' + num
    separators = []
    for i in range(len(num)):
        if i  % 3 == 0: separators.append(len(num) - i)
    newnum = ''
    for i in range(len(num)):
        sep = ' ' if i in separators else ''
        newnum = newnum  + sep + num[i]
    supsep = len (newnum) - 23
    result = ''
    for i in range(len(newnum)):
        sep = '·' if i == supsep else ''
        result = result + sep + newnum[i]
    return result
