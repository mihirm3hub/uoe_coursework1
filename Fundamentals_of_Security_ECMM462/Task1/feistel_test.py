import sys
import re

def encrypt(input_bit, rounds, roundkeys):
   
    leftPart = input_bit[:4]  
    rightPart = input_bit[4:]  
    
    for i in range(rounds):
        round_key = roundkeys[i]
        round_result = f"{int(rightPart, 2) | int(round_key, 2):04b}"
        new_leftPart = rightPart
        new_rightPart = f"{int(leftPart, 2) ^ int(round_result, 2):04b}"
        leftPart, rightPart = new_leftPart, new_rightPart
    return leftPart + rightPart  

def decrypt(input_bit, rounds, roundkeys):
    leftPart = input_bit[:4] 
    rightPart = input_bit[4:]  
    
    for i in range(rounds - 1, -1, -1):
        round_key = roundkeys[i]
        round_result = f"{int(leftPart, 2) | int(round_key, 2):04b}"
        new_rightPart = leftPart
        new_leftPart = f"{int(rightPart, 2) ^ int(round_result, 2):04b}"
        leftPart, rightPart = new_leftPart, new_rightPart

    return leftPart + rightPart  

def main(argv):
    opts = [opt for opt in argv[1:] if opt.startswith("-")]
    args = [arg for arg in argv[1:] if not arg.startswith("-")]
    
    c = re.compile('^[01]{8}$')
    try:
        input_bit = args.pop(0)
    except IndexError:
        raise SystemExit("Usage: {argv[0]} [-d] input rounds roundkey1 roundkey2 ...")
    if not c.fullmatch(input_bit):
        raise SystemExit("input is not a valid bit string")

    try:
        rounds = int(args.pop(0))
    except IndexError:
        raise SystemExit("Usage: {argv[0]} [-d] input rounds roundkey1 roundkey2 ...")
    except ValueError:
        raise SystemExit("rounds is not a valid number")

    if(len(args) < rounds):
        raise SystemExit("Usage: {sys.argv[0]} [-d] input rounds roundkey1 roundkey2 ...")

    roundkeys = args
    c = re.compile('^[01]{4}$')
    if not all(c.search(elem) for elem in roundkeys):
        raise SystemExit("round key is not a valid bit string")


    
    if "-d" in opts:
        result = decrypt(input_bit, rounds, roundkeys)
    else:
        result = encrypt(input_bit, rounds, roundkeys)

    print("Result:", result)
    
if __name__ == "__main__":
    main(sys.argv)