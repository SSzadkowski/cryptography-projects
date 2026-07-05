from utils import letter_to_num, num_to_letter

def encrypt(text, key):
    text = text.upper()
    key = key.upper()
    result = []

    for i, c in enumerate(text):
        p = letter_to_num(c) #zamiana znaku na liczbe
        k = letter_to_num(key[i % len(key)]) # klucz cykliczny KLUCZKLUCZ -> 0123401234

        cipher = (p + k) % 26 # do liczby(znaku) dodajemy przesuniecie klucza
        result.append(num_to_letter(cipher)) #zamiana z powrotem na litere

    return ''.join(result)


def decrypt(text, key):
    text = text.upper()
    key = key.upper()
    result = []

    for i, c in enumerate(text):
        c_val = letter_to_num(c) #kryptogram na liczby
        k = letter_to_num(key[i % len(key)]) #klucz cykliczny

        plain = (c_val - k) % 26 #odwrócenie szyfrowania (odjęcie przesuniecia)
        result.append(num_to_letter(plain))

    return ''.join(result)