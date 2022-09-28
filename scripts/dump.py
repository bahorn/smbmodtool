import sys

target = sys.argv[1]
offset = int(sys.argv[2], 16)
count = int(sys.argv[3])
output = sys.argv[4]

with open(target, 'rb') as target_f:
    target_f.seek(offset)
    data = target_f.read(count)

with open(output, 'wb') as output_f:
    output_f.write(data)
