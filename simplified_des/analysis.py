from collections import Counter
import math
from utils import block_to_str


def analyze_blocks(blocks):
    strings = [block_to_str(block) for block in blocks] #zamiana bloków na stringi
    counter = Counter(strings) #zliczanie wystąpień (ECB ma duzo powtórzeń)

    total = len(strings) #liczba wszystkich bloków
    unique = len(counter) #liczba unikalnych bloków
    repeated = total - unique #liczba powtórzonych bloków

    entropy = 0.0 #wzór Shannona, który mierzy "losowość, chaos".
    for count in counter.values():
        p = count / total
        entropy -= p * math.log2(p)

    return {
        "total": total,
        "unique": unique,
        "repeated": repeated,
        "entropy": entropy,
        "counter": counter,
    }


def print_analysis(name, blocks):
    stats = analyze_blocks(blocks)

    print(f"\n{name}")
    print("-" * 40)
    print("Liczba bloków:", stats["total"])
    print("Liczba unikalnych bloków:", stats["unique"])
    print("Liczba powtórzeń:", stats["repeated"])
    print("Entropia:", round(stats["entropy"], 4))
    print("\nRozkład bloków:")

    for block, count in stats["counter"].most_common():
        print(f"{block} : {count}")