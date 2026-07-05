from utils import permute, left_shift

#permutacje:
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6] #miesza bity
P8 = [6, 3, 7, 4, 8, 5, 10, 9] #bierze 10 bitow wybiera 8


def generate_subkeys(key): # funkcja generujaca podklucze k1 i k2
    if len(key) != 10:
        raise ValueError("Klucz musi mieć dokładnie 10 bitów.")

    p10 = permute(key, P10) #Pierwsza permutacja p10
    left, right = p10[:5], p10[5:] #podział na lewą i prawą część

    left1 = left_shift(left, 1) #przesuniecie lewej czesci o 1 w lewo
    right1 = left_shift(right, 1) #przesuniecie prawej czesci o 1 w lewo
    k1 = permute(left1 + right1, P8) #8 bitowy klucz K1

    left2 = left_shift(left1, 2) #LS2
    right2 = left_shift(right1, 2) #LS2
    k2 = permute(left2 + right2, P8) # 8 bitowy podklucz K2

    return k1, k2