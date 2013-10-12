# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import unittest

from binascii import unhexlify

from bitcoin.base58 import *


def load_test_vector(name):
    with open(os.path.dirname(__file__) + '/data/' + name, 'r') as fd:
        for testcase in json.load(fd):
            yield testcase

class Test_base58(unittest.TestCase):
    def test_encode_decode(self):
        for exp_bin, exp_base58 in load_test_vector('base58_encode_decode.json'):
            exp_bin = unhexlify(exp_bin.encode('utf8'))

            act_base58 = encode(exp_bin)
            act_bin = decode(exp_base58)

            self.assertEqual(act_base58, exp_base58)
            self.assertEqual(act_bin, exp_bin)

    def test_invalid_base58_exception(self):
        with self.assertRaises(InvalidBase58Error):
            decode('#')

class Test_CBitcoinAddress(unittest.TestCase):
    def test_encode_decode(self):
        for exp_bin, exp_addr in load_test_vector('cbitcoinaddress_encode_decode.json'):
            exp_bin = unhexlify(exp_bin.encode('utf8'))

            act_addr = CBitcoinAddress(exp_bin)
            act_bin = CBitcoinAddress.from_str(exp_addr)

            self.assertEqual(str(act_addr), exp_addr)
            self.assertEqual(bytes.__str__(act_bin), exp_bin)

# WARNING: Never import the private keys contained in 
# data/cwalletimportformat_encode_decode.json into a wallet, some wallets may use them as a change address.
# Many people are able to see these private keys and it is likely they are being watched for deposits.

class Test_CWalletImportFormat(unittest.TestCase):
    def test_encode_decode(self):
        for exp_bin, exp_addr in load_test_vector('cwalletimportformat_encode_decode.json'):
            exp_bin = unhexlify(exp_bin.encode('utf8'))

            act_addr = CWalletImportFormat(exp_bin)
            act_bin = CWalletImportFormat.from_str(exp_addr)

            self.assertEqual(str(act_addr), exp_addr)
            self.assertEqual(bytes.__str__(act_bin), exp_bin)
