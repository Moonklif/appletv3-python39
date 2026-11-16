# CPython 3.9.25 for Apple TV 3

[Deutsch](#deutsch) · [English](#english)

## Deutsch

### Status

Experimenteller, gerätespezifischer CPython-3.9.25-Build für ein jailbroken
Apple TV 3. Die hier dokumentierten Ergebnisse stammen aus dem geprüften
Build- und Testverlauf; sie sind keine allgemeine Kompatibilitätszusage.

| Eigenschaft | Bestätigter Wert |
| --- | --- |
| Gerät | AppleTV3,2 |
| Architektur | ARMv7 |
| Systemmeldung | Darwin 14.0.0 |
| Produktversion | Apple TV Software 8.4.4 |
| Build-Ziel | `armv7-apple-ios8.4` |
| Deployment Target | iOS 8.4 |
| CPython | 3.9.25 |

### Bestätigte Ergebnisse

- Der Build erzeugte 63 Erweiterungsmodule.
- Diese Erweiterungen wurden einzeln mit `ldid` signiert.
- Auch der Interpreter benötigte `ldid -S`, bevor `python --version`
  erfolgreich lief.
- Erfolgreich getestet wurden die Imports von `json`, `socket`,
  `asyncio`, `http.server`, `sqlite3` (SQLite 3.8.5), `zlib`,
  `bz2` und `pyexpat`.
- Ein lokaler HTTP-Server antwortete mit HTTP 200 auf
  `127.0.0.1:18080`.

### Patch-Status

Ein getesteter, 219 Zeilen langer `setup.py`-Diff wurde im Buildverlauf
festgehalten. Er behandelt insbesondere Darwin/`darwin-arm`, gequotete
`-isysroot`-Pfade, Apple LLVM, Cross-Compile-Pfade sowie die
Readline/Curses-Ausnahme und deaktiviert auf `darwin-arm` die nicht
unterstützten Module `_ctypes` und `_ctypes_test`.

Im Verlauf sind außerdem die Anforderungen für einen idempotenten Patch-Runner
für `configure.ac` und das generierte `configure` dokumentiert:
Darwin-Cross-Compile-Erkennung, `darwin-arm`, die
`readelf`-Ausnahme, `MACOSX_DEFAULT_ARCH=armv7` und die
Readline-Ausnahme. Die vollständigen Patch- und Runner-Dateien sind jedoch
nicht im aktuellen Repository vorhanden und werden deshalb nicht als Dateien
oder ausführbare Anleitung ausgegeben. Details:
[Build- und Patch-Status](docs/BUILD-STATUS.md).

### Einschränkungen

- Dieses Repository enthält weder CPython-Quellen noch ein geprüftes
  Binär- oder Release-Artefakt.
- SSL/TLS bzw. OpenSSL wurde im verfügbaren Testverlauf **nicht** bestätigt.
  Das getestete Modulverzeichnis enthält kein `ssl`; sichere
  Netzwerkverbindungen dürfen daher nicht vorausgesetzt werden.
- Es gibt keinen belegten End-to-End-Buildbefehl, keine verifizierten
  Toolchain-/SDK-Versionen und keinen wiederhergestellten Original-Patch.
- PHP ist nicht Bestandteil dieses Projekts.
- Die Resultate gelten nur für den beschriebenen jailbroken AppleTV3,2 und
  nicht für andere Apple-TV-Modelle oder Firmwarestände.

### Wiederherstellung

Für einen reproduzierbaren Build fehlen weiterhin die tatsächlich verwendeten
CPython-Quellen, der originale `setup.py`-Patch, die
`configure.ac`/`configure`-Patch-Runner, die genaue Toolchain-Konfiguration
und die zugehörigen Testprotokolle. Erst nach deren Prüfung sollen sie als
Dateien oder Befehle veröffentlicht werden.

## English

### Status

An experimental, device-specific CPython 3.9.25 build for a jailbroken
third-generation Apple TV. The results documented here come from the reviewed
build and test record; they are not a general compatibility guarantee.

| Property | Confirmed value |
| --- | --- |
| Device | AppleTV3,2 |
| Architecture | ARMv7 |
| System report | Darwin 14.0.0 |
| Product version | Apple TV Software 8.4.4 |
| Build target | `armv7-apple-ios8.4` |
| Deployment target | iOS 8.4 |
| CPython | 3.9.25 |

### Confirmed results

- The build produced 63 extension modules.
- Those extensions were individually signed with `ldid`.
- The interpreter itself required `ldid -S` before `python --version`
  succeeded.
- Imports passed for `json`, `socket`, `asyncio`, `http.server`,
  `sqlite3` (SQLite 3.8.5), `zlib`, `bz2`, and `pyexpat`.
- A local HTTP server returned HTTP 200 at `127.0.0.1:18080`.

### Patch status

A tested 219-line `setup.py` diff is recorded in the build history. It covers
Darwin/`darwin-arm`, quoted `-isysroot` paths, Apple LLVM,
cross-compilation paths, and the Readline/Curses exception; it also disables
the unsupported `_ctypes` and `_ctypes_test` modules on `darwin-arm`.

The history also records requirements for an idempotent patch runner for
`configure.ac` and generated `configure`: Darwin cross-compilation
detection, `darwin-arm`, a `readelf` exception,
`MACOSX_DEFAULT_ARCH=armv7`, and the Readline exception. The complete patch
and runner files are not present in this repository, so they are not published
as files or executable instructions. See
[build and patch status](docs/BUILD-STATUS.md).

### Limitations

- This repository contains neither CPython sources nor a verified binary or
  release artifact.
- SSL/TLS and OpenSSL were **not** confirmed in the available test record.
  The listed tested modules do not include `ssl`; secure network connections
  must therefore not be assumed.
- There is no evidenced end-to-end build command, verified toolchain/SDK
  version, or recovered original patch.
- PHP is not included in this project.
- The results apply only to the described jailbroken AppleTV3,2, not to other
  Apple TV models or firmware versions.

### Restoration

A reproducible build still requires the actual CPython source tree, original
`setup.py` patch, `configure.ac`/`configure` patch runners, exact
toolchain configuration, and associated test logs. Only after reviewing them
should they be published as files or commands.
