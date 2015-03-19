#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Search for ext2 filesystems in raw devices.

from __future__ import print_function

import struct
import mmap

def find_all(s, sub, start=0):
    """Yield indices in s where sub is found."""
    while True:
        i = s.find(sub, start)
        if i > -1:
            yield i
            start = i + 1
        else:
            break

def find_superblocks(s, start=0):
    """Yield (offset, superblock) tuples."""

    superblock = Superblock()
    for offset in find_all(s, '\x53\xef', start):
        data = s[offset:offset+20]
        if len(data) < 20:      # EOF
            continue
        superblock.update(data)
        if superblock.is_valid():
            yield offset, superblock

def scan_file(file_obj, start=0):
    """Yield (offset, superblock) tuples."""
    map = mmap.mmap(file_obj.fileno(), 0, access=mmap.ACCESS_READ)
    for offset, superblock in find_superblocks(map, start):
        yield offset, superblock
    map.close()

class Superblock():
    """Superblock object."""
    def __init__(self, data=None):
        self.magic = None
        self.state = None
        self.errors = None
        self.os = None
        if data is not None:
            self.update(data)

    def update(self, data):
        fields = struct.unpack('<HHHHIII', data)
        self.magic = fields[0]
        self.state = fields[1]
        self.errors = fields[2]
        self.os = fields[6]

    def is_valid(self):
        if self.magic != 0xef53:
            return False
        if not self.state in (1, 2, 4):
            return False
        if not self.errors in (1, 2, 3):
            return False
        return True

if __name__ == '__main__':

    import argparse

    oses = {
        'linux':        0,
        'hurd':         1,
        'masix':        2,
        'freebsd':      3,
        'lites':        4
        }

    argparser = argparse.ArgumentParser(
        description='Search for ext2, ext3 and ext4 filesystems' \
        ' in raw devices.')
    argparser.add_argument('file', type=argparse.FileType('rb'))
    argparser.add_argument('-s', '--skip', type=int, default=0,
                           help='skip the first SKIP bytes')
    argparser.add_argument('-o', '--os', type=str,
                           choices=oses.keys(),
                           default=None,
                           help='match creator OS '
                           '(useful to avoid false positives)')

    args = argparser.parse_args()

    print("scanning `{:s}'... C-c to abort (may take a while)".format(
        args.file.name))

    if args.os is None:
        match_os = lambda s: True
    else:
        os = oses[args.os]
        match_os = lambda s: s == os

    try:
        for offset, superblock in scan_file(args.file, start=args.skip):
            if match_os(superblock.os):
                print('match found at offset {:d}; '
                      'possible ext filesystem at offset {:d}'.format(
                          offset, offset - 56 - 1024))
    except KeyboardInterrupt:
        print('aborted.')
    finally:
        args.file.close()
