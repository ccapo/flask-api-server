from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import base64
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--private', default='private_key.pem', help='Filename for private key')
parser.add_argument('--msg', help='Message to sign with private key', required=True)
parser.add_argument('--signed', default=None, help='Optional signed output file')

def sign(keypair, msg):
    # Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
    # Message should in include unique identifier (e.g. counter or UUID) and random salt
    hash256 = SHA256.new(msg)
    signer = PKCS115_SigScheme(keyPair)
    signature = signer.sign(hash256)

    return base64.b64encode(signature).decode('utf-8')

if __name__ == '__main__':
    args = parser.parse_args()

    # load private key
    with open(args.private, 'r') as f:
        keyPair = RSA.import_key(f.read())

    with open(args.msg, 'r') as f:
        msg = f.read().encode('utf-8')

    signed_msg = sign(keyPair, msg)

    if args.signed == None:
        print(signed_msg)
    else:
        with open(args.signed, 'w') as f:
            f.write(signed_msg)