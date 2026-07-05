from utils import permute, xor_bits, bits_to_int, int_to_bits
from key_schedule import generate_subkeys

#definicje permutacji
IP = [2, 6, 3, 1, 4, 8, 5, 7] #wstępne przemieszanie bitów
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6] #odwrotność IP
EP = [4, 1, 2, 3, 2, 3, 4, 1] #permutacja rozszerzająca (prawy blok 4 bity a klucz rundy 8 bitow)
P4 = [2, 4, 3, 1] #ostatnia permutacja wyników z s boxow

#S-Boxy
S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2],
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3],
]


def sbox_lookup(bits4, sbox): #funkcja odczytu z tabeli S box
    row = bits_to_int([bits4[0], bits4[3]]) #wyznaczenie wiersza b1 b4
    col = bits_to_int([bits4[1], bits4[2]]) #wyznaczenie kolumny b2 b3
    value = sbox[row][col] #odczyt z tabeli s box
    return int_to_bits(value, 2) #zamiana na bity


def fk(bits8, subkey): #funkcja rundy fk()
    left = bits8[:4] #podział na lewa czesc
    right = bits8[4:] #podział na prawa czesc

    expanded = permute(right, EP) #permutacja rozszerzająca prawej części
    mixed = xor_bits(expanded, subkey) #mieszanie danych z kluczem

    left4 = mixed[:4] #podział połowy do S0
    right4 = mixed[4:] #podział połowy do S1

    s0_out = sbox_lookup(left4, S0) #przejscie przez S box 0 4bity -> 2 bity
    s1_out = sbox_lookup(right4, S1) #przejscie przez s box 1

    p4 = permute(s0_out + s1_out, P4) #permutacja wyników z s boxów
    new_left = xor_bits(left, p4) #XOR z lewa połowa

    return new_left + right #prawa strona nie jest zmieniana


def switch_halves(bits8):
    return bits8[4:] + bits8[:4] #zamiana półbloków SW


def encrypt_block(plaintext_block, key10): #szyfrowanie
    if len(plaintext_block) != 8:
        raise ValueError("Blok tekstu jawnego musi mieć 8 bitów.")

    k1, k2 = generate_subkeys(key10) #generowanie kluczy

    state = permute(plaintext_block, IP) #permutacja wstępna IP
    state = fk(state, k1) #Runda pierwsza z kluczem k1
    state = switch_halves(state) #zamiana półbloków SW
    state = fk(state, k2) #Runda druga z kluczem K2
    state = permute(state, IP_INV) #permutacja końcowa (odwrotna do IP)

    return state #Zwraca kryptogram


def decrypt_block(ciphertext_block, key10): #Odszyfrowanie
    if len(ciphertext_block) != 8:
        raise ValueError("Blok kryptogramu musi mieć 8 bitów.")

    k1, k2 = generate_subkeys(key10)

    state = permute(ciphertext_block, IP)
    state = fk(state, k2)
    state = switch_halves(state)
    state = fk(state, k1)
    state = permute(state, IP_INV)

    return state

"""
IP
fk(K1)
SW
fk(K2)
IP^-1
------- przy odszyforwaniu
IP
fk(K2)
SW
fk(K1)
IP^-1
"""