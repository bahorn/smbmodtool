"""
Modify the story mode structure.

Story modes structure is documented here:
https://craftedcart.github.io/SMBLevelWorkshop/documentation/index.html?page=modifyingStageOrder

Fairly simple, just indexing an array of the following structs:
```
struct storymode_level {
    uint16_t slot;
    uint16_t difficulty;
};
"""
import struct


class StoryMode:
    """
    Patch the story mode structure
    """

    OFFSET = 0x0020B448
    SIZE = 100*4

    def __init__(self, config, src, dst):
        self.config = config
        self.src = src
        self.dst = dst

    def patch(self):
        """
        Copy the src structure and apply the desired modifications.
        """

        data = b''

        with open(f'{self.src}/files/mkb2.main_loop.rel', 'rb') as input_f:
            input_f.seek(self.OFFSET)
            data = input_f.read(self.SIZE)
        data = bytearray(data)

        for name, value in self.config['storymode'].items():
            world = value['world']
            level = value['level']
            slot = value['slot']
            difficulty = value['difficulty']
            offset = 4*((world - 1)*10 + (level - 1))
            data[offset:offset + 4] = struct.pack('>hh', slot, difficulty)

        with open(f'{self.dst}/files/mkb2.main_loop.rel', 'r+b') as output_f:
            output_f.seek(self.OFFSET)
            output_f.write(data)
