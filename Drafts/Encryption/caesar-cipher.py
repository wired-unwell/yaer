from string import printable
import argparse


def encrypt(message, key):
    encrypted_message = ""
    for letter in message:
        encrypted_message += chr(ord(letter) + key)
    return encrypted_message


def decrypt(encrypted_message, key):
    message = ""
    for letter in encrypted_message:
        message += chr(ord(letter) - key)
    return message


def test():
    for message in ["Hello", "Damn", printable]:
        assert (
            decrypt(encrypt(message, 3), 3) == message
        ), "Encryption or Decryption failed on test"
    # assert 1==2, "Encryption or Decryption failed on test (I'm lying, I tested the test/assert function)."
    print(printable)
    print(encrypt(printable, 3))
    print(decrypt(encrypt(printable, 3), 3))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--message")
    parser.add_argument("--key", default=0, type=int)  # required=True,
    parser.add_argument("command", choices=["encrypt", "decrypt"])
    args = parser.parse_args()

    if args.command == "encrypt":
        print(encrypt(args.message, args.key))
    elif args.command == "decrypt":
        print(decrypt(args.message, args.key))
    else:
        print("Unsupprted command")


if __name__ == "__main__":
    main()
