import sys
import struct

def read_lines_batchwise(filename, batch_size=100):
    with open(filename, 'r') as file:
        while True:
            lines = file.readlines(batch_size)
            if not lines:
                break
            yield lines

filename = sys.argv[1]
data = read_lines_batchwise(filename, 1)

positions = []
DELIMITER = '\t'
keys = []
values = []

# Process the file content
for datum in data:
    kvp = datum[0].split(DELIMITER)

    # Skip empty or malformed lines
    if len(kvp) < 2:
        continue

    keys.append(int(kvp[0]))

    # The serialization concern can be dealt with at a higher level.
    value = DELIMITER.join(kvp[1:])
    values.append(value)

# This allows values to be of variable length.
with open('values.bin', 'wb') as file:
    # Add a placeholder header at the beginning so
    # key-misses don't resolve to a zero-index
    file.write(b'VALUES')

    for value in values:
        encoded_text = value.strip().encode('utf-8')
        length_prefix = len(encoded_text)
        positions.append(file.tell())
        file.write(struct.pack('I', length_prefix))  # Write length prefix
        file.write(encoded_text)  # Write the value text

# Write the position of the value in `values.bin` at the key ith byte in `keys.bin`.
with open('keys.bin', 'wb') as file:
    for i in range(len(keys)):
        # Now position[i] corresponds the location of the corresponding value in 'values.bin'
        # Multiply key value by 8 to accommodate 64-bit (8 byte) representation.
        file.seek(keys[i] * 8)
        file.write(struct.pack('<Q', positions[i]))  # Write the position

