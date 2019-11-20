# Crypto
from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256

# Encoding
import base64
import json
import bz2

# Module Import
import sys
from importlib.util import module_from_spec
from importlib.machinery import ModuleSpec

def CryptoExport(imports, key):
    """ Generates a compressed, encrypted, base64 encoded repository of modules"""
    moduledict = dict()
    for filename in imports:
        with open(filename+".py", 'r') as f:
            raw_file = f.read()
            moduledict[filename] = raw_file
    iv = Random.new().read(16)
    cipher = AES.new(sha256(key.encode()).digest(), AES.MODE_CFB, iv)
    c = cipher.encrypt(bz2.compress(json.dumps(moduledict).encode()))
    return base64.b64encode(iv+c)


class CryptoImporter(object):
    """Given a compressed, encryted, base64 encoded repository of modules this allows for imports of them"""

    def __init__(self, msg, key):
        m_raw = base64.b64decode(msg)
        iv, m = m_raw[:16], m_raw[16:]
        cipher = AES.new(sha256(key.encode()).digest(), AES.MODE_CFB, iv)
        dec = bz2.decompress(cipher.decrypt(m)).decode()
        self._modules = dict(json.loads(dec))
        sys.meta_path.append(self)

    def find_module(self, fullname, path):
        if fullname in self._modules.keys():
            return self
        return None

    def load_module(self, fullname):
        if not fullname in self._modules.keys():
            raise ImportError(fullname)
        spec = ModuleSpec(fullname,self)
        new_module = module_from_spec(spec)
        exec(self._modules[fullname],new_module.__dict__)
        sys.modules[fullname] = new_module
        return new_module


if __name__ == "__main__":
    ## Encrypt example
    a = CryptoExport(['cryptoimport'],'key')
    ## See how output looks like
    #print(a)

    ## contains hello world... trust me ^^
    b = b'OADwUuogn0FxdDF4qd74aj60rku5iBJU9qvVwp8QudXIo/E+P97fBiyzUQS0ytQc5Ml6LlCdb6EHY9ie+EQkqOC6sWT2r/tLUZmWjHRA5xoOeYPy52x52rfhWee5EZSFzGT+twZzjCXyYjJ9XAgZI1/yFpqNZm3LAA0='
    ## if you need to check uncomment the next line and stop there...
    #c = CryptoImporter(b,'key');print(c._modules)

    ## Make 'loadable_module' imporable :P
    CryptoImporter(b,'key')

    ## import and use
    from loadable_module import hello
    hello()
