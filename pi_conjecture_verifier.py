import math
from sympy import primerange

def get_pi_digits(n):
    """Get the first n digits of the decimal part of pi."""
    # Convert pi to string and split at the decimal point
    pi_decimal = str(math.pi).split('.')[1]
    return pi_decimal[:n]

def verify_conjecture(pi_digits, n):
    """Find the first prime p and corresponding k that satisfy the conjecture."""
    for p in primerange(2, 90000):         # iterate primes up to a limit
        for k in range(p):                 # iterate k < p
            fraction = (3 * p + 2 * k) / (p + 1)
            # Format with n decimals, split off integer part
            fraction_str = f"{fraction:.{n}f}".split('.')[1]
            if fraction_str == pi_digits:
                return p, k, fraction
    return None, None, None  # no solution found

if __name__ == "__main__":
    n = int(input("Enter the number of digits of pi to consider: "))
    pi_digits = get_pi_digits(n)
    p, k, fraction = verify_conjecture(pi_digits, n)

    if p is not None:
        print(f"Prime p: {p}")
        print(f"Integer k: {k}")
        print(f"Corresponding fraction: {fraction}")
    else:
        print("No solution found.")
