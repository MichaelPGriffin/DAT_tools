import sys
import struct

def lookup(key):
    with open('keys.bin', 'rb') as file:
        # 8 bytes ==> 64 bits
        file.seek(key * 8)
        byte_count = file.read(8)

        if not byte_count:
            print(f'Unable to read `byte_count` bytes in `keys.bin` for key {key}')
            return None
       
        position = struct.unpack('<Q', byte_count)[0]

        if position == 0:
            print("No such key exists in the collection")
            return None


    with open('values.bin', 'rb') as file:
        file.seek(position)
        byte_count = file.read(4)
        
        if not byte_count:
            print(f'No byte_count read in `values.bin` for key {key}')
            return None

        length = struct.unpack('I', byte_count)[0]
        value_data = file.read(length)
        value = value_data.decode('utf-8')
        return value



key = int(sys.argv[1])
print(lookup(key))

