import sys
import socket
import argparse
import binascii
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

HOST = ''
PORT = 9998
SOCKET_LIST = []


def mypad(somenum):
    return ('0' * (4 - len(str(somenum))) + str(somenum))


def genKey():
    key = RSA.generate(4096)
    f = open('mypubkey.pem', 'w+')
    g = open('myprvkey.pem', 'w+')
    # pubkey_pem.write(RSA.exportKey('PEM'))
    pubkey_pem = key.publickey().exportKey()
    prvkey_pem = key.exportKey()
    f.write(pubkey_pem)
    g.write(prvkey_pem)
    f.close()
    g.close()


def signer():
    message = "Hello world"
    key = RSA.importKey(open('myprvkey.pem').read())
    h = SHA256.new(message)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    return(signature)


def sender(s, signature, message):
    signature_hex = binascii.hexlify(signature)
    pad = mypad(len(message))
    pad2 = mypad(len(signature_hex))
    s.send(pad + message + pad2 + signature_hex)


def connect_to_host(dst):
    """ connects to the host 'dst' """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((dst, PORT))
        SOCKET_LIST.append(s)
        return s
    except socket.error:
        print("Could not connect to %s." % dst)
        sys.exit(0)


def parse_command_line():
    """ parse the command-line """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--c", dest="dst", help="destination address")
    parser.add_argument("-g", "--genkey", dest="genkey", action="store_true", default=False, help="generate RSA Key")
    parser.add_argument("-m", "--m", type=str, dest="message", help="message to be signed")

    options = parser.parse_args()

    if not options.dst and not options.genkey:
        parser.print_help()
        parser.error("must specify either genkey or client mode")

    return options


if __name__ == "__main__":
    options = parse_command_line()

    if options.genkey:
        genKey()
    elif options.dst:
        s = connect_to_host(options.dst)
        message = options.message
        sig = signer()
        sender(s, sig, message)
    else:
        assert(False)

    # genKey()
    # sig = signer()
    # signature_hex = binascii.hexlify(sig)
    # message = "Hello world"
    # pad = mypad(len(message))
    # print(pad + message + signature_hex)
