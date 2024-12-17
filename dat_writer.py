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
lines = read_lines_batchwise(filename, 1)

DELIMITER = '\t'

with open('values.bin', 'wb') as values_file, open('keys.bin', 'wb') as keys_file:
    # Add a placeholder header at the beginning so
    # key-misses don't resolve to zero-index.
    values_file.write(b'VALUES')

    for line in lines:
        kvp = line[0].split(DELIMITER)

        # Skip empty or malformed lines
        if len(kvp) < 2:
            continue

        # The value-serialization concern can be dealt with at a higher level.
        value = DELIMITER.join(kvp[1:])
        encoded_text = value.strip().encode('utf-8')
        # Note values can be of variable length.
        value_start_index = values_file.tell()
        length_prefix = len(encoded_text)
        values_file.write(struct.pack('I', length_prefix))
        values_file.write(encoded_text)

        # Write the position of the value in `values.bin` at the key ith byte in `keys.bin`.
        # Multiply key value by 8 to accommodate fixed-length 64 bit (8 byte) representation.
        key = int(kvp[0])
        keys_file.seek(key * 8)
        keys_file.write(struct.pack('<Q', value_start_index))
