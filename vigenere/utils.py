import string

def clean_text(text):
    return ''.join([c.upper() for c in text if c.isalpha()])  # tylko A-Z

def letter_to_num(c):
    return ord(c) - ord('A')  # A=0 ... Z=25

def num_to_letter(n):
    return chr(n + ord('A'))  # 0-25 -> A-Z


