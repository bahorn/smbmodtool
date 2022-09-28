import sys

target = sys.argv[1]
offset = int(sys.argv[2], 16)
patch = sys.argv[3]

patch_data = b''
with open(patch, 'rb') as patch_f:
    patch_data = patch_f.read()

with open(target, 'r+b') as target_f:
    target_f.seek(offset)
    target_f.write(patch_data)
