#################################################
# Group: Parasaus                               #
# Date: 5/5/2023                                #
# Description: Program 6, uses the xor cypher   #
# algorithm to encode and decode messages.      #
#################################################

import sys

# Read the key from the key file in the current directory
with open("./k3y", "rb") as f:
    key = f.read()

# Read the plaintext/ciphertext from stdin
plaintext = sys.stdin.buffer.read()

# Encrypt/decrypt the plaintext/ciphertext using the key
# Repeat the key to match the length of the plaintext/ciphertext
while len(key) < len(plaintext):
    key = "0" + key

ciphertext = bytes([a ^ b for a, b in zip(plaintext, key)])

# Send the generated output to stdout
sys.stdout.buffer.write(ciphertext)
