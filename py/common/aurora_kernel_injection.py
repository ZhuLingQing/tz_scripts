import sys, os
import binascii


def replace_byte(file_path, offset, new_byte):
    if isinstance(new_byte, int):
        new_byte = bytes([new_byte])
    elif isinstance(new_byte, str):
        new_byte = bytes(new_byte, 'utf-8')
    elif not isinstance(new_byte, bytes):
        raise ValueError("new_byte must be an int, str, or bytes")

    with open(file_path, 'r+b') as file:
        file.seek(offset)
        file.write(new_byte)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ARG1: file path name")
        print("ARG2: offset")
        print("ARG3: value")
        sys.exit(1)
    path_name = str(sys.argv[1])
    offset = int(sys.argv[2], 16)
    addr = int(sys.argv[3], 16)
    baddr = addr.to_bytes(4, 'little')
    print("[inject kernel addr] offset: %x, addr: %x %s" % (offset, addr, str(binascii.hexlify(baddr).decode('utf-8'))))
    if offset >= 0x3e0000:
        offset -= 0x3e0000
    replace_byte(path_name, offset, baddr)
