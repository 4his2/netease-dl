# -*- coding: utf-8 -*-

"""
netease-dl.encrypt
~~~~~~~~~~~~~~~~~~

This module provides the encrypt way for NetEase-Music's post request.
"""
import os
import base64
import json
import binascii
from Crypto.Cipher import AES

from .config import modulus, nonce, pub_key


def encrypted_request(text):
    text = json.dumps(text)
    sec_key = create_secret_key(16)
    enc_text = aes_encrypt(aes_encrypt(text, nonce), sec_key)
    enc_sec_key = rsa_encrpt(sec_key, pub_key, modulus)
    data = {'params': enc_text, 'encSecKey': enc_sec_key}
    return data


def aes_encrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + chr(pad) * pad
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext


def rsa_encrpt(text, pubKey, modulus):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)


def create_secret_key(size):
    return binascii.hexlify(os.urandom(size))[:16]
