def permute(bits, table):
    return [bits[i - 1] for i in table] #funkcja permutacji i-1 bo matematycznie od 1 zaczynamy


def left_shift(bits, n):
    n = n % len(bits) #zabezpieczenie przed przesunięciem większym niż długość listy
    return bits[n:] + bits[:n] #cykliczne przesunięcie w lewo


def xor_bits(a, b):
    return [x ^ y for x, y in zip(a, b)] #operacja XOR na bitach


def int_to_bits(value, size=8):
    return [int(x) for x in format(value, f"0{size}b")] #zamiana liczby na liste bitów


def bits_to_int(bits):
    return int("".join(map(str, bits)), 2) #odwrotnosc powyzszego


def text_to_blocks(text):
    data = text.encode("ascii")
    return [int_to_bits(byte, 8) for byte in data] #zamiana tekstu na liste blokow 8-bitowych


def blocks_to_text(blocks):
    data = bytes(bits_to_int(block) for block in blocks)
    return data.decode("ascii") # odwrotność powyzszego


def block_to_str(block):
    return "".join(map(str, block)) #zamiana bloku bitów na stringa