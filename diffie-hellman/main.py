from dh import run_diffie_hellman
from sdes import encrypt_text, decrypt_text
from utils import blocks_to_str, int_to_bits


INPUT_FILE = "plaintext.txt"
ENCRYPTED_FILE = "ciphertext.txt"
DECRYPTED_FILE = "decrypted.txt"


def read_plaintext(filename): #odczyt tekstu jawengo
    with open(filename, "r", encoding="ascii") as file:
        return file.read()


def save_ciphertext(cipher_blocks, filename): #zapis kryptogramu
    with open(filename, "w", encoding="ascii") as file:
        file.write(blocks_to_str(cipher_blocks))


def save_decrypted(text, filename): #zapis odszyfrowanej wiadomosci
    with open(filename, "w", encoding="ascii") as file:
        file.write(text)


def main():
    print("Diffie-Hellman + Simplified DES\n")

    # Etap DIFFIE–HELLMAN

    dh = run_diffie_hellman()

    key10 = int_to_bits(dh.K,size=10)

    print(f"Liczba losowa k = {dh.k}")
    print(f"Liczba pierwsza p = {dh.p}")
    print(f"Generator g = {dh.g}\n")

    print(f"Prywatny klucz Alicji a = {dh.a}")
    print(f"Prywatny klucz Bolka b = {dh.b}\n")

    print(f"Publiczny klucz Alicji A = {dh.A}")
    print(f"Publiczny klucz Bolka B = {dh.B}\n")

    print(f"KA = {dh.KA}")
    print(f"KB = {dh.KB}")

    print("\nKlucze zgodne:", dh.KA == dh.KB)

    print(
        "Klucz S-DES:",
        "".join(map(str, key10))
    )

    # Odczyt pliku
    try:
        plaintext = read_plaintext(INPUT_FILE)

    except FileNotFoundError:
        print(
            f"\nNie znaleziono pliku {INPUT_FILE}"
        )
        return

    print("\nTekst z pliku:")
    print(plaintext)

    # Szyfrowanie

    cipher_blocks = encrypt_text(
        plaintext,
        key10
    )

    save_ciphertext(
        cipher_blocks,
        ENCRYPTED_FILE
    )

    print(
        f"\nKryptogram zapisano do {ENCRYPTED_FILE}"
    )

    # odszyfrowanie

    decrypted = decrypt_text(
        cipher_blocks,
        key10
    )

    save_decrypted(
        decrypted,
        DECRYPTED_FILE
    )

    print(
        f"Odszyfrowany tekst zapisano do {DECRYPTED_FILE}"
    )

    print("\nOdszyfrowana wiadomość:")
    print(decrypted)


if __name__ == "__main__":
    main()