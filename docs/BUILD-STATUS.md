# Build und Tests / Build and tests

Stand / checked: **2026-11-16**.

## Deutsch

Ich baue CPython 3.9.25 für ein jailbroken **AppleTV3,2 (A1469)** mit ARMv7.
Meine getestete Systemversion auf dem Gerät ist **8.4.4**, Darwin 14.0.0.
Das Compilerziel ist `armv7-apple-ios8.4` mit Prefix `/usr/local`.

### Buildumgebung

| Komponente | Version |
| --- | --- |
| Build-Mac | Apple Silicon, ARM64; Darwin 27.2.0 im Buildprotokoll |
| Native Python-Version | CPython 3.9.25 |
| Nativer Compiler | Apple Clang 21.0.0 |
| Ziel-Xcode | 6.4 (6E35b) |
| Zielcompiler | Apple LLVM 6.1.0, clang-602.0.53 |
| SDK | iPhoneOS 8.4 |
| Configure-Basis | GNU Autoconf 2.69; generiertes `configure` direkt patchen |

### Quellen und Patches

Die Quellen stammen aus dem offiziellen `Python-3.9.25.tgz`.
SHA-256: `a7438eabd3a48139f42d4e058096af8d880b0bb6e8fb8c78838892e4ce5583f2`.
Geändert werden ausschließlich `configure`, `configure.ac` und `setup.py`.
Der Setup-Patch hat 219 Zeilen. Die Patches und ihre Vorher-/Nachher-Hashes
liegen unter [`patches/`](../patches/).

### Auf dem Mac geprüft

- Download und SHA-256 der offiziellen Quellen.
- Exakte Patch-Ergebnisse, wiederholte Anwendung, Sicherungskopien und Ablehnung fremder Änderungen.
- Shell- und Python-Syntax.
- Nativer Host-Python-Build, anschließend ARMv7-Cross-Build mit diesem Interpreter.
- Installation in ein separates Verzeichnis mit `make install DESTDIR=…` und Archivierung.
- Statische Prüfung beider Binärarchive: ARMv7-Interpreter, 63 ARMv7-Erweiterungen,
  Mindestziel iOS 8.4, unsigniert; gleicher Satz von Modulnamen.
- Smoke-Test auf dem Mac: Imports und Loopback-HTTP 200. Das prüft den Testcode;
  ein Mac-Test führt keine ARMv7-Module aus.

### Auf dem Apple TV geprüft

Nach Signierung mit `ldid -S`: `python --version`, `json`, `socket`, `asyncio`,
`http.server`, `sqlite3` (SQLite 3.8.5), `zlib`, `bz2`, `pyexpat` sowie ein
HTTP-Server auf `127.0.0.1:18080`. Ein erneuter Gerätetest der veröffentlichten
Pakete steht aus. Nicht alle 63 Erweiterungen wurden einzeln zur Laufzeit geprüft.

### Fehlende Module

| Module | Buildstatus |
| --- | --- |
| `_gdbm`, `_hashlib`, `_ssl`, `_tkinter`, `nis`, `ossaudiodev`, `spwd` | Abhängigkeiten nicht gefunden |
| `_lzma` | Fehlendes `lzma.h` |
| `_ctypes`, `_ctypes_test` | Für `darwin-arm` deaktiviert |
| Readline, Curses | Erkennung für das Cross-Ziel übersprungen |

Python-Wrapper wie `ssl.py` sind ohne native Erweiterung nicht funktionsfähig.
System-OpenSSL und System-TLS von Blackb0x ändern diesen Python-Build nicht.
`ensurepip` ist abgeschaltet.

### Archive und Protokolle

Das Release enthält das Basisarchiv `AppleTV3-Python39-armv7-8.4.4.tar.gz`
und den mit den Buildskripten erzeugten Build `…-rebuilt.tar.gz`. Beide sind
unsigniert. Ihre Dateihashes stehen in `evidence/original-archive.json` und
`evidence/rebuilt-archive.json`. Der Neubau entfernt Bytecode-Caches und enthält
die CPython-Lizenzhinweise. Wegen Zeitstempeln, Buildpfaden und Debugdaten wird
keine Bitgleichheit der beiden Archive erwartet.

[`evidence/`](evidence/) enthält die technischen Buildnachweise. Persönliche
Homepfade und Hostname sind darin ersetzt. Für die Vorbereitung und den Nachbau
siehe [HowTo](HOWTO-DE.md). Die Blackb0x-Geräte-/Firmwareunterstützung ist
unabhängig von der hier getesteten Python-Konfiguration.

## English

I build CPython 3.9.25 for a jailbroken **AppleTV3,2 (A1469)**, ARMv7, tested
with system version **8.4.4**, Darwin 14.0.0. The compiler target is
`armv7-apple-ios8.4`, prefix `/usr/local`.

Build tools: native CPython 3.9.25 on Apple Silicon; Xcode **6.4 (6E35b)**,
Apple LLVM **6.1.0 (clang-602.0.53)** and **iPhoneOS SDK 8.4** for the target.
The official source checksum is listed above. Exactly three upstream files are
patched: `configure`, `configure.ac`, `setup.py`. Do not regenerate configure.

Verified on the Mac: source checksum, exact patch output, repeated application,
backups, rejection of unrelated edits, syntax, native-host build, cross-build
using that interpreter, staged installation and packaging. Static archive
checks show an ARMv7 interpreter and **63 ARMv7 extensions**, minimum iOS 8.4,
unsigned, with matching module names. The smoke test also passed on the Mac;
that checks the test itself, not the ARMv7 runtime.

Device checks covered signing, version output, `json`, `socket`, `asyncio`,
`http.server`, `sqlite3` (SQLite 3.8.5), `zlib`, `bz2`, `pyexpat` and loopback
HTTP on port 18080. Another device test of the release packages is pending;
not all 63 extensions have individual runtime checks.

Missing dependencies: `_gdbm`, `_hashlib`, `_ssl`, `_tkinter`, `nis`,
`ossaudiodev`, `spwd`; `_lzma` lacks `lzma.h`. The patch disables `_ctypes` and
`_ctypes_test` and skips Readline/Curses detection. System OpenSSL or Blackb0x
system TLS does not enable Python SSL. `ensurepip` is disabled.

Both release archives are unsigned. Their per-file hashes and build logs are
in [`evidence/`](evidence/), with home paths and hostname replaced. The rebuilt
archive removes bytecode caches and explicitly includes CPython license notices;
timestamps, build paths and debug data differ. Start with the [HowTo](HOWTO-EN.md).
Blackb0x support and this Python port's tested firmware are separate scopes.
