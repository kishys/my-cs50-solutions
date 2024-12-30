# Mario More

from cs50 import get_int


def main():
    height = get_height()
    for i in range(1, height + 1):
        print(" " * (height - i), end="")
        print("#" * i, end="")
        print("  ", end="")
        print("#" * i)


def get_height():
    while True:
        height = get_int("Height: ")
        if height >= 1 and height <= 8:
            return height


if __name__ == "__main__":
    main()
