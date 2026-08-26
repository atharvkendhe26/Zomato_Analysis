#!/usr/bin/env python3
"""
even_odd.py
Simple program to check whether a number is even or odd.
"""

def is_even(n: int) -> bool:
    """Return True if n is even, False otherwise."""
    return n % 2 == 0


def main():
    try:
        s = input("Enter an integer: ")
        num = int(s)
    except ValueError:
        print("That's not a valid integer.")
        return

    if is_even(num):
        print(f"{num} is even.")
    else:
        print(f"{num} is odd.")


if __name__ == '__main__':
    main()
