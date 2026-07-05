import sys
from utils import clean_text
from vigenere import encrypt, decrypt
from kryptoanalysis import index_of_coincidence, estimate_key_length, recover_key


def read_file(path):
    with open(path, 'r') as f:
        return clean_text(f.read())


if len(sys.argv) == 1:
    mode = input("Mode (encrypt/decrypt/break): ").strip()

    if mode in ["encrypt", "decrypt"]:
        filename = input("Filename: ")
        key = input("Key: ")
        text = read_file(filename)

        if mode == "encrypt":
            cipher = encrypt(text, key)
            #print("CIPHER:", cipher)

            with open("ciphertext.txt", "w") as f:
                f.write(cipher)   

        else:
            plain = decrypt(text, key)
            #print(plain)

            with open("decrypted.txt", "w") as f:
                f.write(plain)

    elif mode == "break":
        filename = input("Filename: ")
        text = read_file(filename)

        ic = index_of_coincidence(text)
        print("IC:", ic)

        key_len = estimate_key_length(text)
        print("Estimated key length:", key_len)

        key = recover_key(text, key_len)
        print("Recovered key:", key)

        plain = decrypt(text, key)
        #print("Decrypted text:")
        #print(plain)


        with open("decrypted.txt", "w") as f:
            f.write(plain)

    sys.exit()


cmd = sys.argv[1]

if cmd == "encrypt":
    key = sys.argv[2]
    text = read_file(sys.argv[3])

    cipher = encrypt(text, key)
    #print(cipher)

    with open("ciphertext.txt", "w") as f:
        f.write(cipher)


elif cmd == "decrypt":
    key = sys.argv[2]
    text = read_file(sys.argv[3])

    plain = decrypt(text, key)
    #print(plain)

    with open("decrypted.txt", "w") as f:
        f.write(plain)


elif cmd == "break":
    text = read_file(sys.argv[2])

    ic = index_of_coincidence(text)
    print("IC:", ic)

    key_len = estimate_key_length(text)
    print("Estimated key length:", key_len)

    key = recover_key(text, key_len)
    print("Recovered key:", key)

    plain = decrypt(text, key)
    #print("Decrypted text:")
    #print(plain)

    with open("decrypted.txt", "w") as f:
        f.write(plain)