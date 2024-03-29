from collections import OrderedDict
import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from hashlib import sha256

import requests
from flask import Flask, jsonify, request, render_template
import base64
from uuid import uuid4


class Transaction:

    def __init__(self, sender_address, recipient_address, value, transaction_inputs):

        self.sender_address = sender_address                                                                                            #To public key του wallet από το οποίο προέρχονται τα χρήματα
        self.receiver_address = recipient_address                                                                                       #To public key του wallet στο οποίο θα καταλήξουν τα χρήματα
        self.amount = value                                                                                                             #το ποσό που θα μεταφερθεί
        self.transaction_id = uuid4().hex                                                                                               #το hash του transaction
        self.transaction_inputs = transaction_inputs                                                                                    #λίστα από Transaction Input 
        self.transaction_outputs = []                                                                                                   #λίστα από Transaction Output
        self.signature = None

    def to_dict(self):
        transaction_dict = OrderedDict()
        transaction_dict['sender_address'] = self.sender_address
        transaction_dict['recipient_address'] = self.receiver_address
        transaction_dict['value'] = self.amount
        transaction_dict['transaction_id'] = self.transaction_id
        transaction_dict['transaction_inputs'] = self.transaction_inputs
        #transaction_dict['transaction_outputs'] = self.transaction_outputs
        #transaction_dict['signature'] = self.signature
        return transaction_dict
        

    def sign_transaction(self, sender_private_key):
        #Sign transaction with private key
        private_key = RSA.importKey(binascii.unhexlify(sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        hash_obj = self.to_dict()
        hash_obj = SHA.new(str(hash_obj).encode('utf8'))
        self.signature = binascii.hexlify(signer.sign(hash_obj)).decode('ascii')