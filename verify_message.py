from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import base64
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--public', default='public_key.pem', help='Filename for public key')
parser.add_argument('--msg', help='Original message', required=True)
parser.add_argument('--signed', help='Signed message to verify with public key', required=True)

def verify(pubkey, msg, signed_msg):
    hash256 = SHA256.new(msg)
    verifier = PKCS115_SigScheme(pubKey)
    try:
        verifier.verify(hash256, signed_msg)
        return True
    except:
        return False

if __name__ == '__main__':
    args = parser.parse_args()

    # load public key
    with open(args.public, 'r') as f:
        pubKey = RSA.import_key(f.read())

    with open(args.signed, 'r') as f:
        token = base64.b64decode(f.read())

    with open(args.msg, 'r') as f:
        msg = f.read().encode('utf-8')

    verified = verify(pubKey, msg, token)
    if verified:
        print("Signature is valid")
    else:
        print("Signature is invalid")