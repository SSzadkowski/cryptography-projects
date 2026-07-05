from collections import Counter
from utils import letter_to_num, num_to_letter, clean_text

EN_FREQ = {
    'A': 0.0816, 'B': 0.0150, 'C': 0.0218, 'D': 0.0434,
    'E': 0.1209, 'F': 0.0231, 'G': 0.0204, 'H': 0.0595,
    'I': 0.0735, 'J': 0.0010, 'K': 0.0069, 'L': 0.0400,
    'M': 0.0262, 'N': 0.0699, 'O': 0.0772, 'P': 0.0183,
    'Q': 0.0011, 'R': 0.0605, 'S': 0.0631, 'T': 0.0915,
    'U': 0.0290, 'V': 0.0112, 'W': 0.0210, 'X': 0.0017,
    'Y': 0.0212, 'Z': 0.0007
}

def index_of_coincidence(text):
    text = clean_text(text) #czyszczenie
    n = len(text) #n - liczba znakow
    freq = Counter(text) #zliczanie liter

    numerator = sum(v * (v - 1) for v in freq.values()) #pary tych samych liter
    denominator = n * (n - 1) # wszyskie możliwe pary zb

    return numerator / denominator if denominator else 0


IC_EXPECTED = 1.6943
def estimate_key_length(text, max_k=8): #zgadnięcie długości klucza
    text = clean_text(text) #czyszczenie tekstu

    best_k = 1
    best_score = float('inf')

    for k in range(1, max_k + 1): #iteracja po długosciach kluczy
        groups = ['' for _ in range(k)] #grupy na litery tekstu

        for i, c in enumerate(text): #petla po literach kryptogramu
            groups[i % k] += c #podzielenie tekstu na k kolumn

        ic_avg = sum(index_of_coincidence(g) for g in groups) / k #dla kazdej kolumny liczone średnie IC

        score = abs(ic_avg - IC_EXPECTED) #liczone odchylenie od oczekiwanego IC

        if score < best_score:
            best_score = score
            best_k = k

    return best_k


def chi_square_score(text): #badanie rozkladu liter
    n = len(text) #liczba liter
    counter = Counter(text) #zliczenie wystapienie liter

    score = 0
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        observed = counter.get(letter, 0) #ile razy litera pojawila sie w tekscie
        expected = EN_FREQ[letter] * n #ile razy litera powinna pojawic sie dla j ang
        score += (observed - expected) ** 2 / expected #suma odchylen liter

    return score


def find_shift(group): #znajdowanie przesuniecia(litery klucza) dla grupy
    group = clean_text(group)

    best_shift = 0
    best_score = float('inf')

    for shift in range(26): #petla po przesunieciach (literach klucza)
        shifted = ''.join(
            num_to_letter((letter_to_num(c) - shift) % 26)
            for c in group
        )

        score = chi_square_score(shifted) #jak bardzo przesuniety tekst przypomina j ang

        if score < best_score:
            best_score = score
            best_shift = shift

    return best_shift


def recover_key(text, key_len): #odtworzenie calego klucza
    text = clean_text(text)
    key = []

    for i in range(key_len): #kazda iteracja odpwiada jednej literze klucza
        group = text[i::key_len] #bierze co k-ty znak (grupowanie kryptogramu)
        shift = find_shift(group) #znajdywanie przesuniecia(litery klucza) dla grupy
        key.append(num_to_letter(shift))

    return ''.join(key)