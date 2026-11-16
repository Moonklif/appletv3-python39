# Build and recovery status / Build- und Wiederherstellungsstand

Recovery and verification date: **2026-11-16**.

## Deutsch

### Was zuvor veröffentlicht war

`main` enthielt bis Commit `8635887` ausschließlich `README.md`, `LICENSE`
und diese Statusnotiz. Es gab vier Commits, einen Branch und kein Release.
Die im [geteilten Chat](https://chatgpt.com/share/6afb2e03-6334-83ed-894b-6c6d8f740cca)
beschriebenen Projektdateien waren nicht ins GitHub-Repository übertragen worden.
Die damalige Aussage, die Originalpatches seien im Repository nicht vorhanden,
war richtig; die Dateien lagen noch auf dem Build-Mac.

### Wiederhergestellte Dateien

| Fund | Prüfung / Veröffentlichung |
| --- | --- |
| `Python-3.9.25.tgz` | Bytegleich mit erneut heruntergeladenem offiziellen Python-Archiv; SHA-256 im Fetchskript und Release |
| CPython-Quellbaum | Keine fehlenden Upstream-Dateien; exakt drei Upstream-Dateien verändert: `configure`, `configure.ac`, `setup.py` |
| `setup.py-armv7-ios.patch` | Original mit 219 Zeilen; bytegleich mit aus den Quellen neu erzeugtem Diff unter `patches/setup.py.patch` |
| `configure` und `configure.ac` | Diffs direkt zwischen offiziellen Originaldateien und dem vorhandenen Quellstand, keine aus Chaterinnerung erfundenen Patches |
| `config.site`, `config.status`, `Makefile` | Vier Cacheantworten, tatsächliche Compilerflags und Configure-Optionen wiedergefunden; daraus neue Buildskripte erstellt |
| Originales Installationsarchiv | SHA-256 und Hash jedes regulären Archivmitglieds in `evidence/original-archive.json` |
| Build- und Installationslogs | Veröffentlicht unter `evidence/`; persönliche Homepfade und Hostname ersetzt |

Zusätzliche Quelldateien waren nur Zwischensicherungen der drei Änderungen
und Autoconf-Cachedateien. Für den Nachbau werden die offiziellen Quellen plus
die drei vollständigen Patches benötigt. Der frühere Chat-Runner wird nicht
als wiederhergestellt ausgegeben; `scripts/apply-patches.py` ist ein neues,
geprüftes Werkzeug für die tatsächlich gefundenen Diffs.

### Bestätigte Werkzeuge

| Komponente | Wert / Nachweis |
| --- | --- |
| Ziel-Xcode | 6.4, Build 6E35b, aus `Contents/version.plist` |
| Ziel-SDK | iOS 8.4, aus `SDKSettings.plist` |
| Zielcompiler | Apple LLVM 6.1.0, clang-602.0.53; Compileraufruf und Buildlogs |
| Toolchainpfad | `/Volumes/Xcode/Xcode.app/Contents/Developer/…` |
| Host | Apple Silicon, ARM64; Darwin 27.2.0 im Buildprotokoll |
| Nativer Host-Python | CPython 3.9.25; ursprünglicher Host-Build mit Apple Clang 21.0.0 |
| Configure-Generierung | GNU Autoconf 2.69; für den Nachbau nicht neu generieren |
| Ziel | `armv7-apple-ios8.4`, Deployment Target 8.4, Prefix `/usr/local` |

Xcode-6.4-Downloadlinks und Apple-Anmeldehinweise stehen in den
[Bauanleitungen](BUILD-DE.md).

### Neue Prüfungen auf dem Mac

- Offizielle Quellen erneut heruntergeladen und mit lokalem Quellarchiv verglichen.
- Patches auf echten Upstream-Dateien angewendet: alle drei Ergebnisse exakt
  bytegleich mit dem vorhandenen Quellbaum.
- Zweite Anwendung unverändert; unbekannte Änderungen werden vor dem Schreiben
  abgelehnt; Originaldateien gesichert; Shell- und Python-Syntax geprüft.
- Frischer ARMv7-Cross-Build mit dem neuen `build-ios.sh` erfolgreich.
- Neues Installationsarchiv mit `make install DESTDIR=…` erzeugt.
- Original und Neubau statisch geprüft: Interpreter plus 63 `.so`-Module sind
  ARMv7, Mindestziel iOS 8.4; unsigniert. Zusätzlich liegt eine ARMv7-Objektdatei bei.
- Beide Archive enthalten denselben Satz von 63 Erweiterungsmodulnamen.
- Neues `build-host.sh` hat einen nativen CPython-3.9.25-Interpreter erfolgreich
  gebaut und in ein separates Arbeitsverzeichnis installiert. Anschließend
  liefen Cross-Build und Paketierung mit genau diesem neuen Host-Python erneut
  erfolgreich; dieses Ergebnis ist das veröffentlichte Neubauarchiv.
- Smoke-Test auf dem **Mac-Host** ausgeführt: Imports und Loopback-HTTP 200
  erfolgreich. Dies prüft den Testcode, nicht die ARMv7-Laufzeit.

Die Archive müssen wegen Zeitstempeln, Buildpfaden, Debugdaten und aufbereiteter
Installation nicht bitgleich sein. `original-archive.json` und
`rebuilt-archive.json` enthalten die separaten Fingerabdrücke. Das Original
bleibt unverändert. Der Neubau entfernt Bytecode-Caches und legt die
CPython-Lizenzhinweise ausdrücklich bei.

### Historische Tests auf dem Apple TV

Aus dem ursprünglichen Geräteverlauf: AppleTV3,2, Darwin 14.0.0, Apple TV
Software 8.4.4. Nach Signierung mit `ldid -S` funktionierten `python --version`,
Imports von `json`, `socket`, `asyncio`, `http.server`, `sqlite3` (SQLite 3.8.5),
`zlib`, `bz2`, `pyexpat` sowie HTTP 200 auf `127.0.0.1:18080`.
Diese Ergebnisse werden als historische Angaben aus dem Arbeitsverlauf geführt;
es gibt keinen neuen Apple-TV-Zugriff und keinen neuen Geräte-Testbericht.
63 gebaute Erweiterungen bedeuten nicht 63 einzeln geprüfte Imports.

### Bekannte fehlende Module

Das Original-Buildlog bestätigt:

- Nicht gefunden: `_gdbm`, `_hashlib`, `_ssl`, `_tkinter`, `nis`, `ossaudiodev`, `spwd`.
- Fehlgeschlagen: `_lzma`, weil `lzma.h` fehlt.
- Für `darwin-arm` deaktiviert: `_ctypes`, `_ctypes_test`.
- Readline-/Curses-Erkennung für dieses Ziel übersprungen.

Das Vorhandensein von `ssl.py`, `lzma.py` oder `ctypes/` im Standardbibliotheksbaum
belegt kein funktionsfähiges natives Modul. Es wird kein OpenSSL mitgeliefert;
`ensurepip` wurde abgeschaltet. PHP und MNK-Code waren nicht Teil des
wiederhergestellten Python-Builds. Xcode/SDK werden bei Apple bezogen.

## English

Before recovery, `main` at `8635887` contained only a README, GPL license and
status note: four commits, one branch, no releases. The files described in the
shared chat had not been transferred to GitHub.

The original Mac supplied the CPython source archive, patched source tree,
219-line `setup.py` patch, configure records, build logs and installation
archive. The source archive exactly matches a fresh official download. There
are no missing upstream files and exactly **three modified upstream files**:
`configure`, `configure.ac`, `setup.py`. All three diffs are published and their
before/after hashes are pinned. Extra source-tree files were intermediate
backups and Autoconf caches. The old chat's patch runner was not recovered;
the checked-in patch tool and build scripts are newly written from recovered
files and settings.

Verified target tools: **Xcode 6.4 (6E35b), iOS SDK 8.4, Apple LLVM 6.1.0
(clang-602.0.53)**, targeting `armv7-apple-ios8.4`. Host: Apple Silicon,
Darwin 27.2.0 in build logs, native CPython 3.9.25. Original configure was
generated with Autoconf 2.69; do not regenerate it for this procedure.

New checks used real official source files, verified exact patched output,
repeat application, backups, rejection of unknown edits and syntax. A fresh
cross-build and staged install succeeded. The native host-build helper also
successfully built and installed CPython 3.9.25 in a separate work directory.
Cross-build and packaging were then repeated successfully with this new host
interpreter; that full-pipeline result is the published rebuilt archive.
The smoke-test code passed on the **Mac host**, not on the ARMv7 runtime.

Static inspection found an ARMv7 interpreter, **63 ARMv7 extension modules** and
one ARMv7 object file in both installation archives; minimum iOS is 8.4 and the
binaries are unsigned. Extension module names match. Per-file hashes are
published in `evidence/`. Byte-identical output is not claimed: timestamps,
build paths, debug information and staging differ. The original archive is
preserved unchanged; the rebuild removes bytecode caches and includes CPython
license notices explicitly. Home paths and hostname are redacted in logs.

Historical device checks covered AppleTV3,2, Darwin 14.0.0, Apple TV Software
8.4.4, signing with `ldid -S`, version output, imports of `json`, `socket`,
`asyncio`, `http.server`, `sqlite3` (SQLite 3.8.5), `zlib`, `bz2`, `pyexpat`,
and loopback HTTP 200 on port 18080. **No new device runtime test was run.**
63 built extensions does not mean all 63 imports were individually checked.

Original logs confirm absent `_gdbm`, `_hashlib`, `_ssl`, `_tkinter`, `nis`,
`ossaudiodev`, `spwd`; `_lzma` failed due to missing `lzma.h`. The patch disables
`_ctypes`/`_ctypes_test` and skips Readline/Curses detection for `darwin-arm`.
Python wrapper files do not make those native modules available. No OpenSSL,
PHP, MNK code or Apple toolchain is bundled. `ensurepip` is disabled.
