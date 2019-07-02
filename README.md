# MessageSigner
A program that (1) generates an RSA keypair, (2) writes the public portion of the key to a file, and (3) sends a message over a network, followed by its signature.

Program has the following command-line options:
         signer.py --genkey | --c hostname --m message
That is, the program works in two modes. If the --genkey option is specified, your program should generate a new RSA keypair. The public key must be stored in a file in the current working directory called mypubkey.pem. That is, you should save the key as the contents of this file. Note that mypubkey.pem must not contain the private key. (You may want to store the private key in another file because you’ll need it to sign messages.)
If the -c option is specified, then signer.py should open a TCP connection to port 9998 (not 9999) of hostname and send via that connection a signed copy of message.

– the message itself (This should be unencrypted; there’s no confidentiality here.)
