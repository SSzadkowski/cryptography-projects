from dataclasses import dataclass
import secrets #generuje podobno trudniejsze do przewidywania liczby niz random

# konterener na wyniki, żeby nie było bałaganu
@dataclass
class DHResult:
    k: int
    p: int
    g: int
    a: int
    b: int
    A: int
    B: int
    KA: int
    KB: int
    K: int

#4 rundy czyli (1/4)^4 = 0.39%
def miller_rabin(n, rounds=4): #sprawdzenie czy liczba jest prawdopodobnie pierwsza
    if n < 2:
        return False #liczby mniejsze od 2 nie są pierwsze
    if n in (2, 3):
        return True #2 i 3 są pierwsze
    if n % 2 == 0:
        return False #liczby przyste >2 nie są pierwsze

    # n-1 = 2^s * d
    d = n - 1 #zmniejszenie n o 1
    s = 0 #licznik s
    while d % 2 == 0: #przyklad n = 13 -> d = n-1 = 12. 12/2=6, s=1. 6/2=3, s=2. 2^(s=2)*(d=3)=12
        d //= 2
        s += 1

    for _ in range(rounds): #petla przesłuchiwania swiadkow czy liczba jest prawdopodobnie pierwsza
        a = secrets.randbelow(n - 3) + 2  # [2, n-2] losowanie swiadka MR
        x = pow(a, d, n) #potęgowanie modularne a^d mod n, liczymy reszte z tego dzielenia.
        # jesli n jest liczba pierwsza to ta reszta x powinna byc zazwyczaj 1 lub n-1

        if x == 1 or x == n - 1:
            continue #wiec tutaj git idziemy dalej swiadek nie znalazl oszustwa

        witness_found = True #jesli jednak wynik nie był taki jak powyzej to:
        for _ in range(s - 1): #jeszcze jedna szansa podnosimy x do kwadradu s - 1 razy
            x = pow(x, 2, n) # Podnosimy x do kwadratu i bierzemy resztę z dzielenia przez n
            if x == n - 1: #jesli nagle x = n-1 to liczba jest czysta
                witness_found = False
                break

        if witness_found:
            return False

    return True


def generate_10bit_prime(): #losowa 10 bitowa liczba z zakresu 512-1023 i k 256-511
    while True:
        k = secrets.randbelow(256) + 256 #liczba k z zakresu 256-511
        p = 2 * k + 1 #liczba p=2k+1
        if miller_rabin(p, rounds=4): #jesli przejdzie test to jest prawdopodobnie pierwsza
            return k,p


def prime_factors(n): #rozbicie liczby na czynniki pierwsze
    factors = set() # zbior na liczby pierwsze

    while n % 2 == 0:
        factors.add(2) #jesli n/2=0 to dodajemy 2 to zbioru
        n //= 2 #dzielimy az bedzie nieparzysta

    d = 3 #pozbylismy sie dwojek wiec sprawdzamy dzielniki nieparzyste
    while d * d <= n: #najwiekszy mozliwy uniklany dzielnik nie moze byc wiekszy niz pierwiastek z n
        while n % d == 0: #jesli reszta z dzielenia = 0
            factors.add(d) #to dodajemy liczbe do zbioru
            n //= d #i dzielimy przez ta liczbe az bedzie niepodzielna przez nia
        d += 2 #przeskok do kolejnej liczby nieparzystej

    if n > 1: #jesli po tym powyzszym liczba n jest wieksza od 1 to sama w sobie jest pierwsa
        factors.add(n)

    return factors


def is_primitive_root(g, p, factors_of_p_minus_1):
    for q in factors_of_p_minus_1: #petla po unikalnych czynnikach pierwszych
        if pow(g, (p - 1) // q, p) == 1: #warunek z zadania
            return False
    return True # jesli wynik nie byl = 1 oznacza ze liczba q jest generatorem


def find_generator(p): #funckja znajdujaca generator liczby p
    factors = prime_factors(p - 1) #zbior uniklanych czynnikow pierwszych liczby

    while True:
        g = secrets.randbelow(p - 3) + 2  #wylosowanie kandydata na generator z zakresu od 2 do p-2
        if is_primitive_root(g, p, factors): #jesli zwroci true liczba jest generatorem
            return g


def generate_private_key(p):
    return secrets.randbelow(p - 1) + 1 #losowa liczba od 1 do p-1


'''def derive_10bit_key(shared_secret):
    return [int(bit) for bit in format(shared_secret, "010b")]'''


def run_diffie_hellman():
    k,p = generate_10bit_prime() #generowanie liczby p i k
    g = find_generator(p) #znalezienie generatora g dla liczby p

    a = generate_private_key(p) #alicja losuje tajne a
    b = generate_private_key(p) #bolek losuje tajne b

    A = pow(g, a, p) #obliczanie kluczy publicznych
    B = pow(g, b, p) #-''-

    KA = pow(B, a, p) #tajny klucz alicja
    KB = pow(A, b, p) #tajny klucz bolka

    K = KA
    if KA != KB: #sprawdzenie czy klucze są zgodne, jeśli nie to mamy problem
        raise RuntimeError("Błąd: klucze współdzielone nie są równe.")

    return DHResult( k=k,p=p, g=g, a=a, b=b, A=A, B=B, KA=KA, KB=KB, K=K)