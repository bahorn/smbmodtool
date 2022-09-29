"""
Change bytes at a specific address.
"""
import struct
import binascii


class Patcher:
    """
    Change bytes in a file.
    """

    def __init__(self, target):
        self.target = target

    def patch(self, offset, type, data):
        """
        Write `data` at offset.
        """
        new_data = b''
        if type == 'string':
            new_data = bytes(data, 'ascii')
        elif type == 'float':
            new_data = struct.pack('>f', data)
        elif type == 'bytes':
            new_data = binascii.unhexlify(data)

        with open(self.target, 'r+b') as target:
            target.seek(offset)
            target.write(new_data)
