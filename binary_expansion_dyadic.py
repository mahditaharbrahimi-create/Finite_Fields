#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import math
from decimal import Decimal, getcontext, ROUND_FLOOR
from fractions import Fraction

def compute_pi(n_digits):
    """
    Compute pi to n_digits decimal places via the Gauss–Legendre algorithm.
    """
    getcontext().prec = n_digits + 8
    one, two, four = Decimal(1), Decimal(2), Decimal(4)
    a, b, t, p = one, one / two.sqrt(), one / four, one

    # ~log2(n_digits) iterations for convergence
    for _ in range(int(math.log2(n_digits)) + 1):
        an = (a + b) / two
        b = (a * b).sqrt()
        t -= p * (a - an) ** 2
        a, p = an, p * two

    return (a + b) ** 2 / (four * t)

def safe_eval(expr: str, consts: dict) -> Decimal:
    """
    Safely evaluate a numeric expression using AST.
    Supports: literals, + - * / **, unary +/-, names in consts.
    """
    node = ast.parse(expr, mode='eval').body

    def _eval(n):
        if isinstance(n, ast.BinOp):
            L, R = _eval(n.left), _eval(n.right)
            if isinstance(n.op, ast.Add):   return L + R
            if isinstance(n.op, ast.Sub):   return L - R
            if isinstance(n.op, ast.Mult):  return L * R
            if isinstance(n.op, ast.Div):   return L / R
            if isinstance(n.op, ast.Pow):   return L ** R
        if isinstance(n, ast.UnaryOp):
            val = _eval(n.operand)
            if isinstance(n.op, ast.USub):  return -val
            if isinstance(n.op, ast.UAdd):  return +val
        if isinstance(n, ast.Constant):  # Python 3.8+
            return Decimal(str(n.value))
        if isinstance(n, ast.Num):       # older Pythons
            return Decimal(str(n.n))
        if isinstance(n, ast.Name) and n.id in consts:
            return consts[n.id]
        raise ValueError(f"Unsupported expression node: {n!r}")

    return _eval(node)

def greedy_binary(x_dec: Decimal, p: int) -> str:
    getcontext().prec = p + 10
    i = int(x_dec // 1)
    f = x_dec - i
    bits = []
    for _ in range(p):
        f *= 2
        if f >= 1:
            bits.append("1"); f -= 1
        else:
            bits.append("0")
    return f"{i:b}." + "".join(bits)

def ieee754_binary(x: float, bits: int = 53) -> str:
    fr = Fraction.from_float(x)
    i = fr.numerator // fr.denominator
    rem = fr.numerator - i * fr.denominator
    fb = []
    for _ in range(bits):
        rem *= 2
        if rem >= fr.denominator:
            fb.append("1"); rem -= fr.denominator
        else:
            fb.append("0")
    return f"{i:b}." + "".join(fb)

def dyadic_fraction(x_dec: Decimal, p: int) -> Fraction:
    scaled = (x_dec * (1 << p)).to_integral_value(rounding=ROUND_FLOOR)
    return Fraction(int(scaled), 1 << p)

def main():
    p = int(input("Enter precision p (number of fraction bits): "))
    raw = input("Enter real number x (decimal, expression with pi/e): ").strip()

    # Estimate needed decimal digits to cover p binary bits
    n_dec = int(p * math.log10(2)) + 10
    getcontext().prec = n_dec

    # Prepare constants
    pi_dec = compute_pi(n_dec)
    e_dec  = Decimal(str(math.e))
    consts = {"pi": pi_dec, "e": e_dec}

    # Try simple Decimal, otherwise safe_eval
    try:
        x_dec = Decimal(raw)
    except Exception:
        x_dec = safe_eval(raw, consts)

    # Compute expansions
    greedy = greedy_binary(x_dec, p)
    ieee   = ieee754_binary(float(x_dec))
    dyad   = dyadic_fraction(x_dec, p)

    # Output
    print(f"\nBinary greedy expansion (p={p}): {greedy}")
    print(f"IEEE-754 double (53-bit frac):      {ieee}")
    print(f"Dyadic truncation floor(x·2^{p})/2^{p}: {dyad}  (= {float(dyad)})")

if __name__ == "__main__":
    main()
