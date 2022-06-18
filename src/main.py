from bitarray import bitarray

def gen_48bits_key():
    return bitarray(48)

def lfsr(key):
    shift_result = key[0] ^ key[5] ^ key[9] ^ key[10] ^ key[12] ^ key[14] ^ key[15] ^ key[17] ^ key[19] ^ key[24] ^ key[25] ^ key[27] ^ key[29] ^ key[35] ^ key[39] ^ key[41] ^ key[42] ^ key[43]
    key = key << 1
    key[47] = shift_result
    return key

def fa(a, b, c, d):
    return ((a | b) ^ (a & d)) ^ (c & ((a ^ b) | d))


def fb(a, b, c, d):
    return ((a & b) | c) ^ ((a ^ b) & (c | d))


def fc(a, b, c, d, e):
    return (a | ((b | e) & (d ^ e))) ^ ((a ^ (b & d)) & ((c ^ d) | (b & e)))


if __name__ == "__main__":
    key = gen_48bits_key()
    keystream = ""
    for i in range(32):
        key = lfsr(key)
        bitk = fc(fa(key[9], key[11], key[13], key[15]), fb(key[17], key[19], key[21], key[23]), fb(key[25], key[27], key[29], key[31]), fa(key[33], key[35], key[37], key[39]), fb(key[41], key[43], key[45], key[47]))
        keystream += str(bitk)

    print(keystream)