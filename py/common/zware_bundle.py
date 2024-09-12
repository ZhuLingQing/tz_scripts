#!/usr/bin/env python3

import abc
import argparse
import os
import pickle
import sys
import shutil
import subprocess

from pathlib import Path

from west.commands import WestCommand
from west import log

RESOURCE_FILE_MAXCOUNT = (1024 - 32) // 16 - 1

BUNDLE_USAGE = '''\
west bundle [-h] IMAGE_FILE
           [--res0 RESOURCE_FILE/TAG]
           [--res1 RESOURCE_FILE/TAG]
           ...
'''

BUNDLE_DESCRIPTION = f'''\
Convenience wrapper for bundling multiple images into one image.
'''

@staticmethod
def get_cfg(build_conf, item):
    try:
        return build_conf[item]
    except KeyError:
        return None

@staticmethod
def edt_flash_params(b):
    # Get the EDT Node corresponding to the zephyr,flash chosen DT
    # node; 'b' is the build directory as a pathlib object.
    default_params = (4, 0, 0, 1024)

    # Ensure the build directory has a compiled DTS file
    # where we expect it to be.
    edt_pickle = b / 'zephyr' / 'edt.pickle'
    if not edt_pickle.is_file():
        log.die("can't load devicetree; expected to find:", edt_pickle)

    # Load the devicetree.
    with open(edt_pickle, 'rb') as f:
        edt = pickle.load(f)

    # By convention, the zephyr,flash chosen node contains the
    # partition information about the zephyr image to sign.
    flash = edt.chosen_node('zephyr,flash')

    # Get the flash device's write alignment and offset from the
    # slot0_partition and the size from slot1_partition , out of the
    # build directory's devicetree. slot1_partition size is used,
    # when available, because in swap-move mode it can be one sector
    # smaller. When not available, fallback to slot0_partition (single slot dfu).

    # The node must have a "partitions" child node, which in turn
    # must have child nodes with label slot0_partition and may have a child node
    # with label slot1_partition. By convention, the slots for consumption by
    # imgtool are linked into these partitions.
    if (not flash):
        return default_params

    if 'partitions' not in flash.children:
        return default_params

    partitions = flash.children['partitions']
    slots = {
        label: node for node in partitions.children.values()
                    for label in node.labels
                    if label in set(['slot0_partition', 'slot1_partition', 'code_partition'])
    }

    if 'slot0_partition' not in slots:
        return default_params

    # Die on missing or zero alignment or slot_size.
    if 'write-block-size' not in flash.props:
        return default_params

    align = flash.props['write-block-size'].val
    if align == 0:
        return default_params

    # The partitions node, and its subnode, must provide
    # the size of slot1_partition or slot0_partition partition via the regs property.
    # always use addr of slot0_partition, which is where slots are run
    slot_key = 'slot0_partition'
    if not slots[slot_key].regs:
        return default_params
    slot_addr = slots[slot_key].regs[0].addr
    slot_size = slots[slot_key].regs[0].size
    if slot_size == 0:
        return default_params

    slot_vtoff = 0
    if 'code_partition' in slots:
        code_addr = slots['code_partition'].regs[0].addr
        code_size = slots['code_partition'].regs[0].size
        if (code_addr > slot_addr and (slot_addr + slot_size) == (code_addr + code_size)):
            slot_vtoff = code_addr - slot_addr
        else:
            return default_params

    return (align, slot_addr, slot_size, slot_vtoff)

@staticmethod
def pack(build_dir, args, slot_vtoff):
    maxcount = min(RESOURCE_FILE_MAXCOUNT, (slot_vtoff - 32) // 16 - 1)

    b = Path(build_dir)

    board_path = str(b / 'zephyr' / 'zephyr.bin')

    with open(b.parent.parent / f'{b.parent.name}.bdl', mode='wb') as fimg:
        offset = slot_vtoff
        flags = 0
        # master image info
        size = os.stat(board_path).st_size
        fimg.write(b'img0')
        fimg.write(size.to_bytes(4, byteorder="little"))
        fimg.write(offset.to_bytes(4, byteorder="little"))
        fimg.write(flags.to_bytes(4, byteorder="little"))
        offset += (size + 3) & ~3
        # resource images info
        for i in range(maxcount):
            res_name = getattr(args, 'res%d' % (i))
            if (res_name):
                res_name_tag = res_name.split('/')
                if (len(res_name_tag) == 1):
                    res_name_tag.append('r%03d' % (i))
                res_path = str(b.parent.parent / res_name_tag[0])
                size = os.stat(res_path).st_size
                fimg.write(res_name_tag[1][:4].encode())
                fimg.write(size.to_bytes(4, byteorder="little"))
                fimg.write(offset.to_bytes(4, byteorder="little"))
                fimg.write(flags.to_bytes(4, byteorder="little"))
                offset += (size + 3) & ~3
            else:
                fimg.write(b'\x00\x00\x00\x00')
                fimg.write(b'\x00\x00\x00\x00')
                fimg.write(b'\x00\x00\x00\x00')
                fimg.write(b'\x00\x00\x00\x00')
        # master image
        size = os.stat(board_path).st_size
        with open(board_path, mode='rb') as f:
            fimg.write(f.read())
        pad = ((size + 3) & ~3) - size
        if (pad > 0):
            fimg.write(b'\xFF' * pad)
        # resource images
        for i in range(maxcount):
            res_name = getattr(args, 'res%d' % (i))
            if (res_name):
                res_name_tag = res_name.split('/')
                res_path = str(b.parent.parent / res_name_tag[0])
                size = os.stat(res_path).st_size
                with open(res_path, mode='rb') as f:
                    fimg.write(f.read())
                pad = ((size + 3) & ~3) - size
                if (pad > 0):
                    fimg.write(b'\xFF' * pad)

    return offset

@staticmethod
def sign(build_dir, build_conf, args, align, slot_addr, slot_size, slot_vtoff):
    b = Path(build_dir)

    # Base sign command.
    sign_base = [shutil.which('imgtool'), 'sign'] + [
        '--align', str(align),
        '--header-size', '32',
        '--pad-header',
        '--security-counter', 'auto',
        '--slot-size', str(slot_size)]

    if (get_cfg(build_conf, 'CONFIG_FLASH_SIZE') > 0):
        sign_base.extend(['--rom-fixed', '0x%X' % (get_cfg(build_conf, 'CONFIG_FLASH_BASE_ADDRESS') + slot_addr + slot_vtoff)])
    else:
        sign_base.extend(['--load-addr', '0x%X' % (get_cfg(build_conf, 'CONFIG_SRAM_BASE_ADDRESS') + slot_vtoff)])

    sign_base.extend(args.tool_args)

    img_in = str(b.parent.parent / f'{b.parent.name}.bdl')
    img_out = str(b.parent.parent / f'{b.parent.name}.img')
    subprocess.check_call(sign_base + [img_in, img_out])

    os.remove(img_in)

class Bundle(WestCommand):

    def __init__(self):
        super().__init__(
            'bundle',
            # Keep this in sync with the string in west-commands.yml.
            'bundle multiple images into one image',
            BUNDLE_DESCRIPTION,
            accepts_unknown_args=False)

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(
            self.name,
            help=self.help,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=self.description,
            usage=BUNDLE_USAGE)

        parser.add_argument('-d', '--build-dir', help='board to build for with optional board revision')
        for i in range(RESOURCE_FILE_MAXCOUNT):
            parser.add_argument('--res%d' % (i), help='resource image file %d' % (i))

        group = parser.add_argument_group('tool control options')
        group.add_argument('tool_args', nargs='*', metavar='tool_opt',
                           help='extra option(s) to pass to the signing tool')

        return parser

    def do_run(self, args, ignored):
        self.args = args

        zephyr_base = Path(os.environ.get('ZEPHYR_BASE', Path(__file__).parent.parent.parent))
        sys.path.insert(0, str(zephyr_base / 'scripts' / 'west_commands'))
        sys.path.insert(0, str(zephyr_base / 'scripts' / 'dts' / 'python-devicetree' / 'src'))
        from build_helpers import find_build_dir
        from runners.core import BuildConfiguration

        # Bundle images
        build_dir = find_build_dir(args.build_dir)
        build_conf = BuildConfiguration(build_dir)

        # Flash device write alignment and the partition's slot size
        # come from devicetree:
        align, slot_addr, slot_size, slot_vtoff = edt_flash_params(Path(build_dir))

        offset = pack(build_dir, args, slot_vtoff)
        if (slot_size == 0): # RAM load
            slot_size = (offset + 8192) & ~4095
            slot_vtoff = 1024
        sign(build_dir, build_conf, args, align, slot_addr, slot_size, slot_vtoff)
