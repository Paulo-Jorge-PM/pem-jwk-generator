"""
Description: Generate private/public PEM and convert to JWK format
Author: Paulo Jorge PM
Contact: paulo.jorge.pm@gmail.com
"""

import json
import os
from jwcrypto import jwk  # pip install jwcrypto

# Alternatives:
# One can use online tools like:
# PEM to JWK: https://russelldavies.github.io/jwk-creator/
# PEM gen: https://mkjwk.org/
# Redox Admin Portal has key pairs/JWK generators

# For validation use:
# JWT validator against an online JWK: https://jwt.davetonge.co.uk/
# JWT token validation against a JWK + PEM pair: https://jwt.io/

KEY_NAME = ''

while not KEY_NAME:
     KEY_NAME = input('>>> Input key file name: ')

def generate_private_key() -> None:
    """
    Generate private RS384 PEM key with 2048 size (change -E SHA384 to other type of algo if needed)
    Make sure ssh-keygen is installed and in the PATH
    """
    os.system(f'ssh-keygen -t rsa -b 2048 -E SHA384 -m PEM -P "" -f {KEY_NAME}.key')

def generate_public_from_private_key() -> None:
    """
    Generate public RS384 PEM key from the private key
    Make sure OpenSSL and not LibreSSL is the default lib on PC for openssl and that they are in PATH
    """
    os.system(f'openssl rsa -in {KEY_NAME}.key -pubout -outform PEM -out {KEY_NAME}.key.pub')

def generate_jwk_from_private_key() -> None:
    """
    Convert the private PEM to JWK format
    """
    with open(f'{KEY_NAME}.key', 'r') as f:
        private_key_in_pem = f.read()

    print(">>> Private key PEM: ", private_key_in_pem)

    # Create a JWK object from the PEM
    key = jwk.JWK.from_pem(private_key_in_pem.encode())

    # Export the Private PEM to JWK:
    private_jwk = key.export(private_key=True, as_dict=True)

    with open(f'{KEY_NAME}_private_key_jwk.json', 'w') as f:
        json.dump(private_jwk, f, indent=True)

    print(f">>> JWK at {KEY_NAME}.key.jwk.json: ", private_jwk)

def generate_jwk_from_public_key() -> None:
    """
    Convert the public PEM to JWK format
    """
    with open(f'{KEY_NAME}.key.pub', 'r') as f:
        public_key_in_pem = f.read()

    print(">>> Public key PEM: ", public_key_in_pem)

    # Create a JWK object from the PEM
    key = jwk.JWK.from_pem(public_key_in_pem.encode())

    # Export the public Key to JWK:
    public_jwk = key.export_public(as_dict=True)

    with open(f'{KEY_NAME}.key.pub.jwk.json', 'w') as f:
        json.dump(public_jwk, f, indent=True)

    print(f">>> JWK at {KEY_NAME}.key.pub.jwk.json: ", public_jwk)

if __name__ == '__main__':
    generate_private_key()
    generate_public_from_private_key()
    generate_jwk_from_public_key()
    print('>>> Done!')
