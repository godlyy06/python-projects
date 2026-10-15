import string

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
ALPHABET_SIZE = len(LOWERCASE)


def caesar_cipher(message, shift, mode):
    """Encode or decode a message using the Caesar cipher."""
    if mode == "decode":
        shift = -shift

    result = []

    for char in message:
        if char in LOWERCASE:
            alphabet = LOWERCASE
        elif char in UPPERCASE:
            alphabet = UPPERCASE
        else:
            # Keep spaces, punctuation, and other characters unchanged.
            result.append(char)
            continue

        position = alphabet.index(char)
        result.append(alphabet[(position + shift) % ALPHABET_SIZE])

    return "".join(result)


def main():
    message = input("Enter your message: ")
    mode = input("Enter mode (encode/decode): ").strip().lower()

    if mode not in {"encode", "decode"}:
        print("Invalid mode. Please enter 'encode' or 'decode'.")
        return

    shift = int(input("Enter shift amount: "))
    result = caesar_cipher(message, shift, mode)
    print(f"Your {mode}d message: {result}")

    reverse_mode = "decode" if mode == "encode" else "encode"
    answer = input(f"Want to {reverse_mode}? (Y/N) ").strip().lower()

    if answer == "y":
        reverse_result = caesar_cipher(result, shift, reverse_mode)
        print(f"Your {reverse_mode}d message: {reverse_result}")


if __name__ == "__main__":
    main()