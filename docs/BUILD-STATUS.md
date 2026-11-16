# Build and Patch Status / Build- und Patch-Status

## Deutsch

### Nachweisstand

Diese Notiz trennt die im geteilten Arbeitsverlauf festgehaltenen Ergebnisse
von Dateien, die im Repository tatsächlich vorliegen. Sie ersetzt keinen
vollständig reproduzierbaren Build.

### Dokumentierte Build- und Laufzeitprüfung

- Ziel: CPython 3.9.25 für `armv7-apple-ios8.4` mit Deployment Target
  iOS 8.4 auf AppleTV3,2 (Darwin 14.0.0, Apple TV Software 8.4.4).
- 63 Erweiterungsmodule wurden gebaut und einzeln mit `ldid` signiert.
- Der Interpreter benötigte `ldid -S`; anschließend funktionierte
  `python --version`.
- Erfolgreiche Imports: `json`, `socket`, `asyncio`,
  `http.server`, `sqlite3` (SQLite 3.8.5), `zlib`, `bz2`,
  `pyexpat`.
- Der HTTP-Test lieferte HTTP 200 auf `127.0.0.1:18080`.

Der genaue Signierbefehl mit Dateipfad und der konkrete HTTP-Server-Aufruf
sind nicht im verfügbaren Verlauf festgehalten. Diese Datei macht daraus
absichtlich keine nachstellbare Befehlsfolge.

### setup.py

Der dokumentierte 219-Zeilen-Diff für CPython 3.9.25 umfasst:

- eigene Behandlung von Darwin/`darwin-arm`;
- Deaktivierung von `_ctypes` und `_ctypes_test` für `darwin-arm`;
- robustere Erkennung gequoteter `--sysroot`- und `-isysroot`-Werte;
- Erkennung von Apple LLVM;
- Korrekturen für Cross-Compile-Pfade; und
- das Überspringen der Readline/Curses-Erkennung für `darwin-arm`.

Die Original-Patchdatei liegt in diesem Repository nicht vor. Daher wird der
Diff weder nachgeschrieben noch als vollständig oder anwendbar ausgegeben.

### configure.ac und configure

Der frühere Arbeitsstand beschrieb einen idempotenten Runner für
`configure.ac` und generiertes `configure`, mit Prüfungen auf:

- exakt CPython 3.9.25;
- originale Autoconf-Version 2.69;
- Sicherungskopien;
- bereits angewendete Änderungen; und
- Shell-Syntax nach der Änderung.

Er sollte Darwin-Cross-Compile-Erkennung, `darwin-arm`,
`MACOSX_DEFAULT_ARCH=armv7`, die `readelf`-Ausnahme und die
Readline-Ausnahme umsetzen. Die Runner-Dateien und ihre Tests sind hier nicht
vorhanden; diese Beschreibung ist kein Ersatz für sie.

### Nicht bestätigt

SSL/TLS und OpenSSL sind nicht als funktionierend belegt; `ssl` erscheint
nicht in den bestätigten Importtests. Ebenso fehlen die ursprüngliche
Toolchain-/SDK-Konfiguration, CPython-Quellen, Buildskripte und Binärartefakte.
Nichts davon wird mit dieser Dokumentation veröffentlicht oder behauptet.

## English

### Evidence status

This note separates results recorded in the shared work history from files that
actually exist in the repository. It is not a fully reproducible build guide.

### Recorded build and runtime checks

- Target: CPython 3.9.25 for `armv7-apple-ios8.4` with an iOS 8.4
  deployment target on AppleTV3,2 (Darwin 14.0.0, Apple TV Software 8.4.4).
- 63 extension modules were built and individually signed with `ldid`.
- The interpreter required `ldid -S`; `python --version` then worked.
- Successful imports: `json`, `socket`, `asyncio`, `http.server`,
  `sqlite3` (SQLite 3.8.5), `zlib`, `bz2`, and `pyexpat`.
- The HTTP check returned HTTP 200 at `127.0.0.1:18080`.

The exact signing invocation with its file path and the exact HTTP-server
invocation are not preserved in the available record. This document
intentionally does not turn them into an assumed command sequence.

### setup.py

The recorded 219-line diff for CPython 3.9.25 covers:

- dedicated Darwin/`darwin-arm` handling;
- disabling `_ctypes` and `_ctypes_test` for `darwin-arm`;
- more robust detection of quoted `--sysroot` and `-isysroot` values;
- Apple LLVM detection;
- cross-compilation path fixes; and
- skipping Readline/Curses detection for `darwin-arm`.

The original patch file is not present in this repository, so the diff is not
recreated or presented as complete or applicable.

### configure.ac and configure

The previous work described an idempotent runner for `configure.ac` and
generated `configure`, validating:

- exactly CPython 3.9.25;
- original Autoconf version 2.69;
- backups;
- already-applied changes; and
- shell syntax after modification.

It was intended to implement Darwin cross-compilation detection,
`darwin-arm`, `MACOSX_DEFAULT_ARCH=armv7`, the `readelf` exception, and
the Readline exception. The runner files and their tests are not present here;
this description is not a substitute for them.

### Unconfirmed

SSL/TLS and OpenSSL are not evidenced as working; `ssl` is absent from the
confirmed import tests. The original toolchain/SDK configuration, CPython
sources, build scripts, and binary artifacts are also absent. This
documentation neither publishes nor claims any of them.
