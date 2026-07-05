from utils import permute, left_shift

#definicja permutacji:
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]


def generate_subkeys(key):
    if len(key) != 10:
        raise ValueError("Klucz musi mieć dokładnie 10 bitów.")

    p10 = permute(key, P10) #pierwsza permutacja (wymieszanie klucza)
    left, right = p10[:5], p10[5:] #podział na pół

    left1 = left_shift(left, 1) #przesuniecie o 1 w lewo
    right1 = left_shift(right, 1) #przesuniecie o 1 w lewo
    k1 = permute(left1 + right1, P8) #podklucz pierwszej rundy

    left2 = left_shift(left1, 2) #przesuniecie w lewo dodatkowo o 2
    right2 = left_shift(right1, 2) #przesuniecie w lewo dodatkowo o2
    k2 = permute(left2 + right2, P8) # drugi podklucz 2 rundy

    return k1, k2

#P10
#LS1
#P8 -> K1
#LS2
#P8 -> K2