from __future__ import annotations


def permute(bits, table):
    return [bits[i - 1] for i in table] #funkcja permutacji bitów według tabeli


def left_shift(bits, n):
    n = n % len(bits)
    return bits[n:] + bits[:n] #cykliczne przesuniecie w lewo


def xor_bits(a, b):
    return [x ^ y for x, y in zip(a, b)] #operacja XOR na dwoch listach bitów


def int_to_bits(value, size=8):
    return [int(x) for x in format(value, f"0{size}b")] #zamiana liczby na bity


def bits_to_int(bits):
    return int("".join(map(str, bits)), 2) #zamiana bitów na int, 2 -> zapis bianrny


def text_to_blocks(text):
    data = text.encode("ascii")
    return [int_to_bits(byte, 8) for byte in data] #zamiana tekstu na bloki


def blocks_to_text(blocks):
    data = bytes(bits_to_int(block) for block in blocks)
    return data.decode("ascii") #zamiana bloku na tekst


def block_to_str(block):
    return "".join(map(str, block)) #wypisywanie bloku jako string


def blocks_to_str(blocks):
    return " ".join(block_to_str(block) for block in blocks) #zamiana całej listy blokow w jeden zapis