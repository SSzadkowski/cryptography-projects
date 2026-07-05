from file import read_ascii_text
from utils import text_to_blocks, blocks_to_text, block_to_str
from sdes import encrypt_block, decrypt_block
from modes import ecb_encrypt, ecb_decrypt, cbc_encrypt, cbc_decrypt
from analysis import print_analysis

KEY = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0] #Przykładowy klucz s des
IV = [0] * 8 #poczatkowy jawny wektor IV = 0x00

#podstawowy S-DES - szyfrowanie i odszyfrowanie pojedynczego bloku
def demo_single_block():
    text = input("Podaj dokładnie 1 znak ASCII: ")

    if len(text) != 1:
        print("Trzeba podać dokładnie jeden znak.")
        return

    block = text_to_blocks(text)[0]

    print("\nBlok jawny:", block_to_str(block))

    cipher = encrypt_block(block, KEY)
    print("Po szyfrowaniu:", block_to_str(cipher))

    plain = decrypt_block(cipher, KEY)
    print("Po odszyfrowaniu:", block_to_str(plain))
    print("Odtworzony znak:", blocks_to_text([plain]))


def demo_modes_and_statistics():
    filename = input("Podaj nazwę pliku [input.txt]: ").strip() or "input.txt"
    text = read_ascii_text(filename)
    blocks = text_to_blocks(text)

    print("\nTekst jawny:")
    print(text)

    ecb_cipher = ecb_encrypt(blocks, KEY)
    cbc_cipher = cbc_encrypt(blocks, KEY, IV)

    print_analysis("ECB - analiza statystyczna kryptogramu", ecb_cipher)
    print_analysis("CBC - analiza statystyczna kryptogramu", cbc_cipher)

    ecb_plain = ecb_decrypt(ecb_cipher, KEY)
    cbc_plain = cbc_decrypt(cbc_cipher, KEY, IV)

    print("\nECB po odszyfrowaniu:")
    print(blocks_to_text(ecb_plain))

    print("\nCBC po odszyfrowaniu:")
    print(blocks_to_text(cbc_plain))


def main():
    while True:
        print("\nS-DES")
        print("1. Szyfrowanie i odszyfrowanie pojedynczego bloku")
        print("2. ECB + CBC + analiza statystyczna")
        print("0. Wyjście")

        choice = input("Wybór: ").strip()

        if choice == "1":
            demo_single_block()
        elif choice == "2":
            demo_modes_and_statistics()
        elif choice == "0":
            break
        else:
            print("Niepoprawny wybór.")


if __name__ == "__main__":
    main()