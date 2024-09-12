from ctypes import *
from py_git import git
import sys
import struct
import os


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

def computeChecksum32(bary, seed : int = 0):
    assert len(bary) % 4 == 0, "invalid buffer for checksum32"
    for i in range(0, len(bary), 4):
        seed += int.from_bytes(bary[i:i+4], byteorder='little', signed=False)
    return seed & 0xFFFFFFFF

def checkGfAuroraHardcode(bary):
    hardcode_offset = 0x80
    hardcode_str = str("f32710309583858ba1cf739007300967")
    hardcode_ary = bary[hardcode_offset:hardcode_offset+int(len(hardcode_str)/2)].hex()
    assert hardcode_ary == hardcode_str, "invalid hard code segement"
    return hardcode_ary

class GfAuroraWorkloadSign(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('name', c_char * 16),
        ('version', c_uint32),
        ('checksum32', c_uint32),
        ('size_in_bytes', c_uint32),
        ('tag', c_char * 8),
        ('reserved', c_char * 28),
    ]
    
    def encode(self):
        return string_at(addressof(self), sizeof(self))

    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)
    
def imageSign(fname_i):
    fname_s = fname_i.split('/')[-1].split('.')[0]
    in_b = readBinFile(fname_i)
    sign = GfAuroraWorkloadSign()
    sign.decode(in_b)
    checkGfAuroraHardcode(in_b)
    if 0 == computeChecksum32(in_b):
        return in_b

    if (len(fname_s) > 15):
        sign.name = fname_s.encode('utf-8')[:15]
    else:
        sign.name = fname_s.encode('utf-8')
    sign.size_in_bytes = len(in_b)

    path = os.path.dirname(os.path.abspath(fname_i))
    g = git(path)
    if g.isClean() is True:
        sign.tag = (g.getCommit(True)[0:7]).encode('utf-8')
    else:
        sign.tag = (g.getCommit(True)[0:7] + '*').encode('utf-8')
    sign.checksum32 = 0
    buf = sign.encode()
    chks = computeChecksum32(buf, 0)
    chks = computeChecksum32(in_b[len(buf):], chks)
    sign.checksum32 = ((~chks) & 0xFFFFFFFF) + 1
    print("checksum32 is: %x" % sign.checksum32)
    buf = sign.encode()
    out_b = buf + in_b[len(buf):]
    return out_b

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("arg1: input file name")
        print("arg2: output file name, none means check only.")
        sys.exit(1)
    elif len(sys.argv) == 2:
        fname_i = sys.argv[1]
        fname_o = None
    else:
        fname_i = sys.argv[1]
        fname_o = sys.argv[2]
    fname_s = fname_i.split('/')[-1].split('.')[0]
    print(fname_s)
    in_b = readBinFile(fname_i)
    sign = GfAuroraWorkloadSign()
    sign.decode(in_b)
    checkGfAuroraHardcode(in_b)
    if fname_o == None:
        chks = computeChecksum32(in_b)
        if 0 != chks:
            print("!!!!! invalid checksum (%x) !!!!!" % chks)
        else:
            print("name         :", sign.name.decode('utf-8'))
            print("checksum32   : 0x%x" % sign.checksum32)
            print("size_in_bytes:", sign.size_in_bytes)
            print("branch       :", sign.branch.decode('utf-8'))
            print("tag          :", sign.tag.decode('utf-8'))
            if sign.branch.decode('utf-8')[-1:] == '*':
                print("WARNING: branch is not clean")
    else:
        out_b = imageSign(fname_i)
        writeBinFile(fname_o, out_b)
        print("output to: ", fname_o)
    print(" >>>>> done <<<<<")
    sys.exit(0)