# CPython 3.9.25 for Apple TV 3

[Deutsch](#deutsch) · [English](#english)

## Deutsch

Mit diesem Projekt baue ich **Python 3.9.25 für mein Apple TV 3**.
Meine getestete Konfiguration ist **AppleTV3,2 (A1469), ARMv7, Systemversion
8.4.4**. Das Compilerziel ist `armv7-apple-ios8.4`.

Die Quellen bleiben bei CPython; dieses Repository enthält die nötigen
Patches, Einstellungen und Skripte zum Nachbauen auf einem Mac.

**Hier anfangen: [HowTo – vom Mac und Apple TV bis zum laufenden Python](docs/HOWTO-DE.md)**

Die Anleitung führt der Reihe nach durch:

1. Mac, Kabel und Apple TV vorbereiten.
2. Apple TV bei Bedarf mit [Blackb0x--](https://github.com/regulad/Blackb0x--) jailbreaken und SSH prüfen.
3. Xcode 6.4 und die Mac-Werkzeuge einrichten.
4. Host-Python und ARMv7-Python bauen.
5. Archiv übertragen, installieren, signieren und testen.

[Bauanleitung im Detail](docs/BUILD-DE.md) · [Installation](docs/INSTALL.md) ·
[Downloads](https://github.com/Moonklif/appletv3-python39/releases) ·
[Build und Tests](docs/BUILD-STATUS.md)

### Was funktioniert?

Der Build enthält **63 native Erweiterungsmodule**. Auf dem Apple TV wurden
`json`, `socket`, `asyncio`, `http.server`, `sqlite3` (SQLite 3.8.5), `zlib`,
`bz2`, `pyexpat` und ein lokaler HTTP-Server getestet. Die komplette Baukette
auf dem Mac wurde am 16.11.2026 geprüft.

### Was wird benötigt?

- Ein Mac mit Entwicklerwerkzeugen; auf Apple Silicon ausführbare Intel-Werkzeuge über Rosetta.
- **Xcode 6.4 (6E35b) mit iOS-SDK 8.4**:
  [Apple-Downloadarchiv](https://developer.apple.com/download/all/?q=Xcode%206.4) ·
  [Xcode_6.4.dmg](https://download.developer.apple.com/Developer_Tools/Xcode_6.4/Xcode_6.4.dmg).
- Ein jailbroken AppleTV3,2 mit SSH und `ldid`.

### Einschränkungen

SSL/TLS, `_hashlib`, LZMA und `ctypes` sind in diesem Build nicht verfügbar.
Readline und Curses werden beim Cross-Build übersprungen; `ensurepip` ist
ausgeschaltet. Ein installiertes System-OpenSSL ergänzt Python nicht automatisch
um SSL. Die Archive müssen mit `ldid -S` signiert werden.

Die Release-Pakete wurden auf dem Mac gebaut und statisch geprüft; ein erneuter
Gerätetest dieser Pakete steht aus. Andere Modelle und Firmwarestände sind für
diesen Python-Port nicht getestet. Blackb0x hat eine eigene Kompatibilitätsliste.

[Patches](patches/) · [Buildprotokolle](docs/evidence/) · [Lizenzen](docs/LICENSING.md)

## English

I use this project to build **Python 3.9.25 for my Apple TV 3**.
My tested configuration is **AppleTV3,2 (A1469), ARMv7, system version 8.4.4**,
with compiler target `armv7-apple-ios8.4`.

This repository provides the patches, configuration and Mac build scripts on
top of the official CPython sources.

**Start here: [HowTo – from Mac and Apple TV setup to a running Python](docs/HOWTO-EN.md)**

The guide covers prerequisites, [Blackb0x--](https://github.com/regulad/Blackb0x--),
SSH, Xcode 6.4, native host Python, the ARMv7 build, transfer, installation,
signing and tests, in that order.

[Detailed build guide](docs/BUILD-EN.md) · [Installation](docs/INSTALL.md) ·
[Downloads](https://github.com/Moonklif/appletv3-python39/releases) ·
[Build and tests](docs/BUILD-STATUS.md)

The build contains **63 native extensions**. Device checks covered `json`,
`socket`, `asyncio`, `http.server`, `sqlite3` (SQLite 3.8.5), `zlib`, `bz2`,
`pyexpat` and loopback HTTP. The full Mac build pipeline was checked on 2026-11-16.

Requirements: a Mac with developer tools, working Intel-tool support via Rosetta
on Apple Silicon, **Xcode 6.4 (6E35b) / iOS SDK 8.4** from
[Apple](https://developer.apple.com/download/all/?q=Xcode%206.4), and a jailbroken
AppleTV3,2 with SSH and `ldid`.

SSL/TLS, `_hashlib`, LZMA and `ctypes` are unavailable. Readline/Curses detection
is skipped and `ensurepip` is disabled. A system OpenSSL install does not enable
Python SSL by itself. Sign the archives' binaries using `ldid -S`.

Release packages have been built and statically checked on the Mac; another
device test of these packages is pending. Other models and firmware versions
have not been tested for this Python port. Blackb0x has its own compatibility list.

[Patches](patches/) · [Build logs](docs/evidence/) · [Licenses](docs/LICENSING.md)
