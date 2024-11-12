import sys  # Import sys to access command-line arguments
import re  # Import re for regular expressions


def encrypt(input_bit, rounds, roundkeys):
    """
    Encrypts an 8-bit binary string using a Feistel-like structure.
    
    Parameters:
    - input_bit (str): The 8-bit binary string to encrypt.
    - rounds (int): Number of encryption rounds to apply.
    - roundkeys (list of str): List of 4-bit binary round keys.
    
    Returns:
    - str: Encrypted 8-bit binary string.
    """
    # Split input into two 4-bit halves
    leftPart = input_bit[:4]
    rightPart = input_bit[4:]

    # Apply the number of rounds specified
    for i in range(rounds):
        round_key = roundkeys[i]

        # Round operation: OR right part with the round key
        round_result = f"{int(rightPart, 2) | int(round_key, 2):04b}"

        # Swap and XOR to produce new left and right parts
        new_leftPart = rightPart
        new_rightPart = f"{int(leftPart, 2) ^ int(round_result, 2):04b}"

        # Update left and right parts for the next round
        leftPart, rightPart = new_leftPart, new_rightPart

    # Return final concatenated result of left and right parts
    return leftPart + rightPart


def decrypt(input_bit, rounds, roundkeys):
    """
    Decrypts an 8-bit binary string using a Feistel-like structure.
    
    Parameters:
    - input_bit (str): The 8-bit binary string to decrypt.
    - rounds (int): Number of decryption rounds to apply.
    - roundkeys (list of str): List of 4-bit binary round keys.
    
    Returns:
    - str: Decrypted 8-bit binary string.
    """
    # Split input into two 4-bit halves
    leftPart = input_bit[:4]
    rightPart = input_bit[4:]

    # Reverse the rounds to decrypt
    for i in range(rounds - 1, -1, -1):
        round_key = roundkeys[i]

        # Round operation: OR left part with the round key
        round_result = f"{int(leftPart, 2) | int(round_key, 2):04b}"

        # Swap and XOR to revert to previous left and right parts
        new_rightPart = leftPart
        new_leftPart = f"{int(rightPart, 2) ^ int(round_result, 2):04b}"

        # Update left and right parts for the next round
        leftPart, rightPart = new_leftPart, new_rightPart

    # Return final concatenated result of left and right parts
    return leftPart + rightPart


def main(argv):
    """
    Main function to handle command-line arguments and trigger encryption/decryption.
    
    Parameters:
    - argv (list of str): List of command-line arguments.
    
    Raises:
    - SystemExit: If any input validation fails.
    """
    # Separate options (flags) and arguments (input data)
    opts = [opt for opt in argv[1:] if opt.startswith("-")]
    args = [arg for arg in argv[1:] if not arg.startswith("-")]

    # Regular expression to check for 8-bit binary input
    c = re.compile('^[01]{8}$')
    try:
        input_bit = args.pop(0)
    except IndexError:
        raise SystemExit("Usage: {argv[0]} [-d] input rounds roundkey1 roundkey2 ...")

    # Validate input bit format (must be 8 binary characters)
    if not c.fullmatch(input_bit):
        raise SystemExit("input is not a valid bit string")

    # Validate and retrieve the number of rounds
    try:
        rounds = int(args.pop(0))
    except IndexError:
        raise SystemExit("Usage: {argv[0]} [-d] input rounds roundkey1 roundkey2 ...")
    except ValueError:
        raise SystemExit("rounds is not a valid number")

    # Ensure there are enough round keys for the specified rounds
    if len(args) < rounds:
        raise SystemExit("Usage: {sys.argv[0]} [-d] input rounds roundkey1 roundkey2 ...")

    # Extract round keys and validate format (each key must be 4-bit binary)
    roundkeys = args
    c = re.compile('^[01]{4}$')
    if not all(c.search(elem) for elem in roundkeys):
        raise SystemExit("round key is not a valid bit string")

    # Determine whether to encrypt or decrypt based on option flag
    if "-d" in opts:
        result = decrypt(input_bit, rounds, roundkeys)
    else:
        result = encrypt(input_bit, rounds, roundkeys)

    # Output the final result
    print("Result:", result)


# Entry point for command-line execution
if __name__ == "__main__":
    main(sys.argv)
