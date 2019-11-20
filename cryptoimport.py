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
    # Look for python files and get their source code
    # These are stored in a dict so we can load the code later
    moduledict = dict()
    for filename in imports:
        with open(filename+".py", 'r') as f:
            raw_file = f.read()
            moduledict[filename] = raw_file

    # Now lets prepare the crypto
    # The sha256 lets us use any size of key as input as the output is a valid AES256 key
    # Also generate a Initialization Vector to make precomputation attacks harder
    iv = Random.new().read(16)
    cipher = AES.new(sha256(key.encode()).digest(), AES.MODE_CFB, iv)

    # Now we transform the dict to JSON then compress with bz2 and then encode it with AES
    # python dict -> JSON -> bz2 -> AES256
    c = cipher.encrypt(bz2.compress(json.dumps(moduledict).encode()))

    # Last we concatenate IV and message and base64 encode everything
    return base64.b64encode(iv+c)


class CryptoImporter(object):
    """Given a compressed, encryted, base64 encoded repository of modules this allows for imports of them"""
    def __init__(self, msg, key):
        # First we have to base64 decode and split IV and encrypted message
        raw = base64.b64decode(msg)
        iv, c = raw[:16], raw[16:]

        # Once again prepare the cipher and convert
        # AES256 -> bz2 -> JSON -> python dict
        cipher = AES.new(sha256(key.encode()).digest(), AES.MODE_CFB, iv)
        dec = bz2.decompress(cipher.decrypt(c)).decode()
        self._modules = dict(json.loads(dec))

        # self._modules now contains the original module name and the source code

        # We have to register this CryptoImporter to sys.meta_path
        # This allows python to ask us for modules
        sys.meta_path.append(self)

    def find_module(self, fullname, path):
        # python first tries to find a module before trying to load it
        if fullname in self._modules.keys():
            return self
        return None

    def load_module(self, fullname):
        if not fullname in self._modules.keys():
            raise ImportError(fullname)

        # Build a new module from a specification
        # The new module should know at least it's name and the loader
        spec = ModuleSpec(fullname,self)
        new_module = module_from_spec(spec)

        # Execute the given source code inside the name space of the newly created module
        exec(self._modules[fullname],new_module.__dict__)

        # Finally register the module so it can be used
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

    ## Make 'loadable_module' importable :P
    CryptoImporter(b,'key')

    ## import and use
    from loadable_module import hello
    hello()
