#!/usr/bin/env python3
"""Inspect an Apple TV install archive without executing its binaries."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import struct
import tarfile

def macho(data):
    if data[:4] != b'\xce\xfa\xed\xfe':
        return None
    _, cpu, subtype, kind, ncmds, size, flags = struct.unpack_from('<7I', data)
    pos = 28
    result = dict(cpu=cpu, subtype=subtype, filetype=kind, signed=False, dependencies=[])
    for _ in range(ncmds):
        cmd, length = struct.unpack_from('<2I', data, pos)
        if length < 8 or pos + length > len(data):
            raise ValueError('Invalid Mach-O command')
        if cmd == 0x1d:
            result['signed'] = True
        if cmd == 0x25:
            version = struct.unpack_from('<I', data, pos + 8)[0]
            result['minimum_ios'] = '%d.%d.%d' % (version >> 16, (version >> 8) & 255, version & 255)
        if cmd in (0xc, 0x80000018, 0x8000001f):
            offset = struct.unpack_from('<I', data, pos + 8)[0]
            result['dependencies'].append(data[pos + offset:pos + length].split(b'\0', 1)[0].decode())
        pos += length
    return result

def inspect(path):
    result = dict(archive=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(), files={}, binaries={})
    with tarfile.open(path) as archive:
        for member in archive:
            p = PurePosixPath(member.name)
            if p.is_absolute() or '..' in p.parts or not (member.name == 'usr/local' or member.name.startswith('usr/local/')):
                raise ValueError('Unexpected member: ' + member.name)
            if member.issym() or member.islnk():
                resolved = posixpath.normpath(posixpath.join(str(p.parent), member.linkname) if member.issym() else member.linkname)
                if not resolved.startswith('usr/local/'):
                    raise ValueError('Link leaves install tree: ' + member.name)
            elif member.isfile():
                data = archive.extractfile(member).read()
                result['files'][member.name] = hashlib.sha256(data).hexdigest()
                info = macho(data)
                if info:
                    if info['cpu'] != 12 or (info['subtype'] & 0xffffff) != 9:
                        raise ValueError('Expected ARMv7: ' + member.name)
                    result['binaries'][member.name] = info
            elif not member.isdir():
                raise ValueError('Unsupported archive entry: ' + member.name)
    if 'usr/local/bin/python3.9' not in result['binaries']:
        raise ValueError('Interpreter missing')
    result['extension_count'] = sum(n.endswith('.so') for n in result['binaries'])
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.archive), indent=2, sort_keys=True))
