# Rebuild the transaction trie for block 10467135 with HexaryTrie
#the transaction root for block 10467135
#https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag=0x9fb73f&boolean=true&apikey=YourApiKeyToken
# TransactionRoot = "0xbb345e208bda953c908027a45aa443d6cab6b8d2fd64e83ec52f1008ddeafa58"
import rlp
from rlp.sedes import big_endian_int, binary
import json
import codecs
from trie import HexaryTrie
import binascii

# https://ethereum.stackexchange.com/questions/70584/how-to-build-a-simple-transaction
class Transaction(rlp.Serializable):
    fields = [
        ('nonce', big_endian_int),
        ('gasprice', big_endian_int),
        ('startgas', big_endian_int),
        ('to', binary.fixed_length(20, allow_empty = True)),
        ('value', big_endian_int),
        ('data', binary),
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int)
    ]

    def __init__(self, nonce, gasprice, startgas, to, value, data, v, r, s):
        #to = normalize_address(to, allow_blank = True)
        super(Transaction, self).__init__(nonce, gasprice, startgas, to, value, data, v, r, s)

if  __name__ == '__main__':
    with open('transactions.json', 'r') as f:
        data = f.read()

    parsed_data = json.loads(data)
    t = HexaryTrie(db={})

    for i in range(0, len(parsed_data)):
        pd = parsed_data[i]
        tx = Transaction(int(pd["nonce"], 16), 
                         int(pd["gasPrice"], 16), 
                         int(pd["gas"], 16), 
                         codecs.decode(pd["to"][2:], 'hex'), 
                         int(pd["value"], 16),
                         codecs.decode(pd["input"][2:], 'hex'), 
                         int(pd["v"], 16), 
                         int(pd["r"], 16), 
                         int(pd["s"], 16))

        t[rlp.encode(i)] = rlp.encode(tx)

    print(binascii.hexlify(t.root_hash))