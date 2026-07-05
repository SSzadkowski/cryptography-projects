from sdes import encrypt_block, decrypt_block
from utils import xor_bits
#Jak szyfrować wiele bloków na raz? (tryby szyfrowania)

#ECB = każdy blok szyfrujemy niezależnie, bez żadnych powiązań między blokami
#problem jest taki ze identyczne bloki wejsciowe dają identyczne bloki wyjsciowe
def ecb_encrypt(blocks, key10):
    return [encrypt_block(block, key10) for block in blocks]

def ecb_decrypt(blocks, key10):
    return [decrypt_block(block, key10) for block in blocks]

#Każdy szyfrowny blok zależy od poprzedniego szyfrogramu
def cbc_encrypt(blocks, key10, iv=None):
    if iv is None:
        iv = [0] * 8 #początkowy wektor iv jest jawny 0x00

    result = []
    prev = iv #poprzedni szyfrogram

    for block in blocks:
        xored = xor_bits(block, prev) #XOR z poprzednim szyfrogramem
        cipher = encrypt_block(xored, key10) #szyfrowanie
        result.append(cipher) #dodawanie szyfrogramu
        prev = cipher #aktualizacja poprzedniego szyfrogramu

    return result

def cbc_decrypt(blocks, key10, iv=None):
    if iv is None:
        iv = [0] * 8

    result = []
    prev = iv

    for block in blocks: #petla po blokach szyfrogramu
        plain_temp = decrypt_block(block, key10) #odszyfrowanie s des
        plain = xor_bits(plain_temp, prev) #cofnięcie operacji XOR
        result.append(plain) #dodanie odszyfrowanego bloku
        prev = block #zamiana poprzednika

    return result