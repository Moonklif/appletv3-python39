#!/usr/bin/env python3
"""Apply recovered patches only to exact original CPython 3.9.25 files."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def apply(source):
    source = Path(source).resolve()
    manifest = json.loads((ROOT / 'patches/SHA256.json').read_text())
    pending = []
    # Check every input before mutating any file.
    for name, hashes in manifest.items():
        target = source / name
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest == hashes['patched']:
            print('Already patched:', name)
        elif digest == hashes['original']:
            backup = source / (name + '.appletv3-original')
            if backup.exists() and backup.read_bytes() != target.read_bytes():
                raise ValueError('Refusing to overwrite different backup: ' + str(backup))
            subprocess.run(['patch', '--dry-run', '-p1', '-i', str(ROOT / 'patches' / (name + '.patch'))], cwd=source, check=True)
            pending.append(name)
        else:
            raise ValueError('Unexpected source contents (requires CPython 3.9.25): ' + name)
    for name in pending:
        shutil.copy2(source / name, source / (name + '.appletv3-original'))
        subprocess.run(['patch', '-p1', '-i', str(ROOT / 'patches' / (name + '.patch'))], cwd=source, check=True)
        assert hashlib.sha256((source / name).read_bytes()).hexdigest() == manifest[name]['patched']
    subprocess.run(['sh', '-n', str(source / 'configure')], check=True)
    compile((source / 'setup.py').read_bytes(), str(source / 'setup.py'), 'exec')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    apply(parser.parse_args().source)
