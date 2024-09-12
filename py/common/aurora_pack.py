from ctypes import *
from image_sign import *
from crc32 import crc32
import sys, struct, os

def readBinFile(file_path):
    try:
        binfile = open(file_path,'rb')
        size = os.path.getsize(file_path)
        data = binfile.read(size)
        binfile.close()
        return data
    except:
        assert False, "file not exist"

def writeBinFile(file_path, bary):
    try:
        binfile = open(file_path,'wb')
        binfile.write(bary)
        binfile.close()
    except:
        assert False, "file not exist"

class GfAuroraMcpFwSign(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('signature', c_char * 8),
        ('size_bytes', c_uint32),
        ('header_size_bytes', c_uint32),
        ('header_version_major', c_uint16),
        ('header_version_minor', c_uint16),
        ('ip_version_major', c_uint16),
        ('ip_version_minor', c_uint16),
        ('ucode_version_major', c_uint16),
        ('ucode_version_minor', c_uint16),
        ('ucode_size_bytes', c_uint32),
        ('ucode_array_offset_bytes', c_uint32),
        ('crc32', c_uint32)
    ]
    
    def encode(self):
        return string_at(addressof(self), sizeof(self))

    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("arg1: input binary file name")
        print("arg2: output signed binary file name, None means check only")
        sys.exit(1)
    elif len(sys.argv) == 2:
        fname_i = sys.argv[1]
        fname_o = None
    else:
        fname_i = sys.argv[1]
        fname_o = sys.argv[2]
    in_b = readBinFile(fname_i)
    if in_b[0:8] == b"WF.IA.TL":
        print("input is already signed")
        sign = GfAuroraMcpFwSign()
        sign.decode(in_b)
        print("Crc32 is: 0x%X" %sign.crc32)
        sys.exit(0)
    elif fname_o == None:
        print("Invalid signature:", in_b[0:8])
        sys.exit(1)
    in_b = imageSign(fname_i)
    if (len(in_b) + 40) % 64:
        in_b += bytearray(64 - (len(in_b) + 40) % 64)
    sign = GfAuroraMcpFwSign()
    sign.signature = "WF.IA.TL".encode('utf-8')
    sign.size_bytes = len(in_b) + 40
    sign.header_size_bytes = 40
    sign.header_version_major = 1
    sign.header_version_minor = 0
    sign.ip_version_major = 1
    sign.ip_version_minor = 0
    sign.ucode_version_major = 1
    sign.ucode_version_mino = 0
    sign.ucode_size_bytes = len(in_b)
    sign.ucode_array_offset_bytes = 40
    sign.crc32 =  crc32(in_b) ^ 0xFFFFFFFF
    out_b = sign.encode() + in_b
    writeBinFile(fname_o, out_b)
    print("output to: %s. crc32: 0x%08X" %( fname_o, sign.crc32))
    print(" >>>>> done <<<<<")
    sys.exit(0)