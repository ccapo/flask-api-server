from Crypto.PublicKey import RSA
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--bits', type=int, default=1024, help='RSA key-pair size in bits (default: 1024)')
parser.add_argument('--private', default='private_key.pem', help='Filename for private key')
parser.add_argument('--public', default='public_key.pem', help='Filename for public key')

if __name__ == '__main__':
    args = parser.parse_args()

    # Generate 1024-bit RSA key pair (private + public key)
    keyPair = RSA.generate(bits=args.bits)
    pubKey = keyPair.public_key()

    # Export private and public keys
    privKey = keyPair.export_key()

    with open(args.private, 'w') as out:
        out.write(privKey.decode('utf-8'))

    with open(args.public, 'w') as out:
        out.write(pubKey.export_key().decode('utf-8'))