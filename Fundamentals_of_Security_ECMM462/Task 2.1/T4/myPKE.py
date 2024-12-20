import random

def generatePKE(N):
    # Create matrices M1, M2 & M3
    M1 = random.sample(range(1, N + 1), N)
    M2 = [random.sample(range(1, N + 1), N) for _ in range(N)]
    M3 = [[0] * N for _ in range(N)]
    
    # Construct M3 to related to expression M3(M2(M1(k), p), k) = p
    # encryption = M2(public_key, p)
    # decryption M3(encrypted, k) = p
    for k in range(1, N + 1):
        public_key = M1[k - 1]  # M1(k) in 1-indexed terms
        for p in range(1, N + 1):
            encryption = M2[public_key - 1][p - 1]  
            M3[encryption - 1][k - 1] = p 
    
    return M1, M2, M3

def encrypt(k, p, M1, M2):
 
    public_key = M1[k - 1]

    # Encrypt the plaintext p using M2 
    ciphertext = M2[public_key - 1][p - 1]
    return ciphertext

def decrypt(k, ciphertext, M3):
    # Decrypt the ciphertext using M3
    plaintext = M3[ciphertext - 1][k - 1]
    return plaintext

# Example
N = 5
M1, M2, M3 = generatePKE(N)

private_key = 3
plaintext = 4

# Encryption
ciphertext = encrypt(private_key, plaintext, M1, M2)
print("Ciphertext:", ciphertext)

# Decryption
decrypted_plaintext = decrypt(private_key, ciphertext, M3)
print("Decrypted Plaintext:", decrypted_plaintext)

# Matrices
print("M1:", M1)
print("M2:")
for row in M2:
    print(row)
print("M3:")
for row in M3:
    print(row)
