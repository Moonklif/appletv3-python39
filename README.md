# CPython 3.9.25 for Apple TV 3

[Deutsch](#deutsch) · [English](#english)

## Deutsch

Experimenteller CPython-3.9.25-Port für ein **jailbroken AppleTV3,2**, ARMv7,
Apple TV Software **8.4.4**, Build-Ziel `armv7-apple-ios8.4`.

Die zuvor fehlenden Originaländerungen wurden vom Build-Mac wiederhergestellt.
Das Repository enthält jetzt alle drei Quellpatches, die Cross-Compile-Konfiguration,
Build- und Paketierungsskripte, Signierungsanleitung, Laufzeittest und Buildnachweise.
Ein frischer Cross-Build mit diesen Patches wurde am 16.11.2026 auf dem Mac geprüft.

**Start:** [Bauanleitung auf Deutsch](docs/BUILD-DE.md) ·
[Installation und Tests](docs/INSTALL.md) ·
[Downloads / Vorabversion](https://github.com/Moonklif/appletv3-python39/releases)

### Voraussetzungen

- macOS mit nativer CPython-3.9.25-Buildumgebung (aktuelle Mac-Entwicklerwerkzeuge).
- **Xcode 6.4 (6E35b), iOS-SDK 8.4, Apple LLVM 6.1.0** für das ARMv7-Ziel.
  [Bei Apple herunterladen](https://developer.apple.com/download/all/?q=Xcode%206.4)
  oder [Xcode_6.4.dmg direkt bei Apple](https://download.developer.apple.com/Developer_Tools/Xcode_6.4/Xcode_6.4.dmg).
  Apple-Anmeldung erforderlich. Xcode und SDK werden von Apple bezogen.
- Ein bereits jailbroken AppleTV3,2 mit Shell-Zugang und `ldid` zum Signieren.

### Umfang und Grenzen

- Ursprünglicher Build: **63 native Erweiterungsmodule**; Imports von `json`,
  `socket`, `asyncio`, `http.server`, `sqlite3` (SQLite 3.8.5), `zlib`, `bz2`
  und `pyexpat` sowie HTTP 200 sind im früheren Geräteverlauf dokumentiert.
- `_ssl` und `_hashlib` wurden nicht gebaut; `_lzma` scheiterte am fehlenden
  `lzma.h`. `_ctypes`, `_ctypes_test`, Readline und Curses sind für dieses
  Cross-Ziel deaktiviert/übersprungen. Kein funktionsfähiges HTTPS oder pip
  voraussetzen; `ensurepip` ist abgeschaltet.
- Das wiederhergestellte Originalarchiv ist **unsigniert**. Interpreter und
  Erweiterungsmodule müssen mit `ldid -S` signiert werden.
- Neuer Mac-Build und statische ARMv7-Prüfung sind von historischen Gerätetests
  getrennt dokumentiert. Es wurde kein neuer Test auf dem Apple TV durchgeführt.
- Kein Jailbreak-Installer, kein PHP und keine MNK-Anwendung enthalten.
  Andere Apple-TV-Modelle und Firmwarestände wurden nicht geprüft.

[Prüfstand und Herkunft](docs/BUILD-STATUS.md) ·
[Patches](patches/) · [Technische Nachweise](docs/evidence/) ·
[Lizenzen](docs/LICENSING.md)

## English

Experimental CPython 3.9.25 for a **jailbroken AppleTV3,2**, ARMv7, Apple TV
Software **8.4.4**, targeting `armv7-apple-ios8.4`.

The missing source changes have been recovered from the build Mac. This
repository now includes all three source patches, cross-compilation settings,
build and packaging scripts, signing instructions, a runtime smoke test and
build evidence. A fresh cross-build using these patches was checked on the Mac
on 2026-11-16.

**Start:** [English build guide](docs/BUILD-EN.md) ·
[Installation and tests](docs/INSTALL.md) ·
[Downloads / prerelease](https://github.com/Moonklif/appletv3-python39/releases)

### Requirements

- macOS with native CPython 3.9.25 build tools (current Mac developer tools).
- **Xcode 6.4 (6E35b), iOS SDK 8.4, Apple LLVM 6.1.0** for the ARMv7 target.
  [Download from Apple](https://developer.apple.com/download/all/?q=Xcode%206.4)
  or [Apple's Xcode_6.4.dmg link](https://download.developer.apple.com/Developer_Tools/Xcode_6.4/Xcode_6.4.dmg).
  Apple sign-in is required. Obtain Xcode and the SDK directly from Apple.
- An already jailbroken AppleTV3,2, shell access and `ldid` for signing.

### Scope and limitations

The original build contains **63 native extension modules**. Historical device
checks covered `json`, `socket`, `asyncio`, `http.server`, `sqlite3` (SQLite
3.8.5), `zlib`, `bz2`, `pyexpat` and loopback HTTP 200. `_ssl` and `_hashlib`
were not built; `_lzma` failed because `lzma.h` was missing. `_ctypes`,
`_ctypes_test`, Readline and Curses are disabled/skipped for this cross-target.
Do not assume working HTTPS or pip; `ensurepip` is disabled.

The recovered original archive is **unsigned**: sign the interpreter and
extensions with `ldid -S`. New Mac builds and static ARMv7 checks are documented
separately from historical device checks; no new Apple TV runtime test was run.
No jailbreak installer, PHP or MNK application is included. Other models and
firmware versions have not been checked.

[Evidence and provenance](docs/BUILD-STATUS.md) · [Patches](patches/) ·
[Technical evidence](docs/evidence/) · [Licenses](docs/LICENSING.md)
