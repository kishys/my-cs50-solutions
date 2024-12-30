# Credit More

from cs50 import get_string


def main():
    card_number = get_string("Number: ")
    if is_valid(card_number):
        if is_amex(card_number):
            print("AMEX")
        elif is_mastercard(card_number):
            print("MASTERCARD")
        elif is_visa(card_number):
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")


def is_valid(number):
    total = 0
    reverse_digits = number[::-1]

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def is_amex(number):
    return len(number) == 15 and (number.startswith("34") or number.startswith("37"))


def is_mastercard(number):
    return len(number) == 16 and (number[:2] in ["51", "52", "53", "54", "55"])


def is_visa(number):
    return len(number) in [13, 16] and number.startswith("4")


if __name__ == "__main__":
    main()
