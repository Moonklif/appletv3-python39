# Licenses and sources

The repository's existing [GPL-3.0 license](../LICENSE) is retained for the
project's own tooling and documentation. CPython and its bundled components
retain their upstream copyright and license notices; see
[CPython 3.9.25 LICENSE](../LICENSES/CPython-3.9.25.txt). Patch files contain
upstream CPython context and project modifications. Project patch date: 2026-11-16.
Changes cover Darwin ARM cross-compilation, SDK path discovery and disabling
unsupported extension detection; they are not an official Python release.

The official, unmodified CPython source archive is available at:
[Python-3.9.25.tgz](https://www.python.org/ftp/python/3.9.25/Python-3.9.25.tgz).
Its SHA-256 is pinned in `scripts/fetch-source.sh`; the exact source is also
included with the release. Apply `patches/configure.patch`,
`patches/configure.ac.patch` and `patches/setup.py.patch` to obtain the project
source state. These are the three modified upstream source files.

Xcode 6.4, the iOS SDK, Apple firmware, jailbreak software and `ldid` are not
redistributed here. The Apple download links are in the build guides. OpenSSL is not linked into this Python build and is not part of the release.

Deutsch: Die bestehende Projektlizenz bleibt erhalten. CPython und enthaltene
Drittkomponenten behalten ihre Originalhinweise. Die vollständigen
CPython-Lizenzhinweise und die exakten Quellpatches liegen bei. Apple-Werkzeuge
werden direkt bei Apple bezogen und nicht über dieses Projekt verteilt.
