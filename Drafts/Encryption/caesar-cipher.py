#!/usr/bin/env python3

from string import printable
import argparse

# l = len(printable)
l = 96


def encrypt(message, key):
    encrypted_message = ""
    for letter in message:
        encrypted_message += chr((ord(letter) + key - 32) % l + 32)
    return encrypted_message


def decrypt(encrypted_message, key):
    message = ""
    for letter in encrypted_message:
        message += chr((ord(letter) - key - 32) % l + 32)
    return message


def test():
    for message in ["Hello World", "Damn", "Man miravam be bazar"]:
        assert (
            decrypt(encrypt(message, 3), 3) == message
        ), "Encryption or Decryption failed on test"
    # assert 1==2, "Encryption or Decryption failed on test (I'm lying, I tested the test/assert function)."
    print(printable)
    print(encrypt(printable, 3))
    print(decrypt(encrypt(printable, 3), 3))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", default="")
    parser.add_argument("--key", default=0, type=int)  # required=True,
    parser.add_argument("command", choices=["encrypt", "decrypt", "brute", "test"])
    args = parser.parse_args()

    if args.command == "encrypt":
        if args.key == 0:
            print("\x1b[0;33mKey omitted, doing nothing.\x1b[0m")
        else:
            args.key = args.key % l
        print(encrypt(args.message, args.key))
    elif args.command == "decrypt":
        if args.key == 0:
            print("\x1b[0;33mKey omitted, doing nothing.\x1b[0m")
        else:
            args.key = args.key % l
        print(decrypt(args.message, args.key))
    elif args.command == "brute":
        for i in range(96):
            print(f"\x1b[0;31m{i}.\x1b[0m " + decrypt(args.message, i))
    elif args.command == "test":
        test()
    else:
        print("Unsupprted command")


if __name__ == "__main__":
    main()
