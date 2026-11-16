"""Validate against actual official CPython files, not synthetic fixtures."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('patcher', ROOT / 'scripts/apply-patches.py')
patcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patcher)

class PatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.source = Path(self.tmp.name)
        archive = Path(os.environ.get('CPYTHON_ARCHIVE', ROOT / 'work/Python-3.9.25.tgz'))
        assert hashlib.sha256(archive.read_bytes()).hexdigest() == 'a7438eabd3a48139f42d4e058096af8d880b0bb6e8fb8c78838892e4ce5583f2'
        self.manifest = json.loads((ROOT / 'patches/SHA256.json').read_text())
        with tarfile.open(archive) as tar:
            for name in self.manifest:
                (self.source / name).write_bytes(tar.extractfile('Python-3.9.25/' + name).read())

    def test_exact_application_and_repeat(self):
        patcher.apply(self.source)
        first = {p.name: p.read_bytes() for p in self.source.iterdir()}
        patcher.apply(self.source)
        self.assertEqual(first, {p.name: p.read_bytes() for p in self.source.iterdir()})
        for name, hashes in self.manifest.items():
            self.assertEqual(hashlib.sha256((self.source / name).read_bytes()).hexdigest(), hashes['patched'])
            self.assertEqual(hashlib.sha256((self.source / (name + '.appletv3-original')).read_bytes()).hexdigest(), hashes['original'])

    def test_modified_source_rejected_before_changes(self):
        path = self.source / 'setup.py'
        path.write_bytes(path.read_bytes() + b'\n# unrelated edit\n')
        before = {p.name: p.read_bytes() for p in self.source.iterdir()}
        with self.assertRaises(ValueError):
            patcher.apply(self.source)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.source.iterdir()})

if __name__ == '__main__':
    unittest.main()
