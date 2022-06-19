from bitarray import bitarray
from tabulate import tabulate
from time import sleep


def gen_48bits_key():
    return bitarray(48)


def gen_16bits_key():
    return bitarray(16)


def lfsr(key):
    shift_result = key[0] ^ key[5] ^ key[9] ^ key[10] ^ key[12] ^ key[14] ^ key[15] ^ key[17] ^ key[19] ^ key[24] ^ key[25] ^ key[27] ^ key[29] ^ key[35] ^ key[39] ^ key[41] ^ key[42] ^ key[43]
    key = key << 1
    key[47] = shift_result

    print(f"LFSR: {printable_key(key)} | Shift Result -> {shift_result}")

    sleep(0.3)

    return key


def fa(a, b, c, d):
    return ((a | b) ^ (a & d)) ^ (c & ((a ^ b) | d))


def fb(a, b, c, d):
    return ((a & b) | c) ^ ((a ^ b) & (c | d))


def fc(a, b, c, d, e):
    return (a | ((b | e) & (d ^ e))) ^ ((a ^ (b & d)) & ((c ^ d) | (b & e)))


def gen_keystream(key):
    keystream = ""
    for _ in range(32):
        key = lfsr(key)
        bitk = fc(fa(key[9], key[11], key[13], key[15]), fb(key[17], key[19], key[21], key[23]), fb(key[25], key[27], key[29], key[31]), fa(key[33], key[35], key[37], key[39]), fb(key[41], key[43], key[45], key[47]))
        keystream += str(bitk)

    return keystream


def lfsr_nonce(key):
    shift_result = key[0] ^ key[2] ^ key[3] ^ key[5]
    key = key << 1
    key[15] = shift_result

    return key


def gen_nonce(key):
    nonce = ""
    for _ in range(32):
        key = lfsr_nonce(key)
        nonce += str(key[15])

    return nonce


def printable_key(key):
    pkey = ""

    for k in key:
        pkey += str(k)

    return pkey


def print_table(key, key2, keystream, nonce):
    headers = ["48 BITS KEY", "16 BITS KEY", "KEYSTREAM (32 BITS)", "NONCE (32 BITS)"]
    table = [headers, [printable_key(key), printable_key(key2), keystream, nonce]]

    print(tabulate(table, headers="firstrow", tablefmt="psql"))


if __name__ == "__main__":

    key = gen_48bits_key()
    key2 = gen_16bits_key()
    keystream = gen_keystream(key)
    nonce = gen_nonce(key2)

    print_table(key, key2, keystream, nonce)
