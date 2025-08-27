# greedy_truncation2.py

import math

def greedy_truncation(x: float, k: int) -> list:
    """
    Return the first k bits of the greedy binary expansion
    of x in [0,1), using only the fractional part.
    """
    x = x % 1.0
    bits = []
    for _ in range(k):
        x *= 2
        bit = int(x)
        bits.append(bit)
        x -= bit
    return bits

if __name__ == "__main__":
    print("N ->", greedy_truncation(1/2, 1))          # [1]
    print("Z ->", greedy_truncation(3/4, 2))          # [1, 1]
    print("Q ->", greedy_truncation(5/8, 4))          # [1, 0, 1, 0]

    # R  in F_{2^16} → 16 bits of √2’s fractional part
    print("R ->", greedy_truncation(math.sqrt(2), 16))
