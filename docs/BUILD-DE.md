# Auf dem Mac bauen

Für die komplette Reihenfolge einschließlich Mac-Vorbereitung und Jailbreak:
[HowTo](HOWTO-DE.md).

Ziel ist ein jailbroken **AppleTV3,2 mit Apple TV Software 8.4.4**. Die
Compiler-Zielversion ist iOS **8.4**, nicht `8.4.4`. Alle folgenden Befehle
werden zunächst auf dem Mac ausgeführt. Der Mac erhält keine ARMv7-Installation
in seinem `/usr/local`; die Paketierung verwendet ein separates Staging-Verzeichnis.

## 1. Werkzeuge beschaffen

Für den nativen Host-Python-Build werden funktionierende aktuelle
Mac-Entwicklerwerkzeuge benötigt. Für den Apple-TV-Build wird separat
**Xcode 6.4 (6E35b)** mit **iOS-SDK 8.4** und **Apple LLVM 6.1.0
(clang-602.0.53)** verwendet. Mit dieser Kombination habe ich den ARMv7-Build geprüft. Ein aktuelles Xcode ersetzt die alte
ARMv7-Toolchain hier nicht.

- [Offizielles Apple-Downloadarchiv, Suche Xcode 6.4](https://developer.apple.com/download/all/?q=Xcode%206.4)
- [Xcode_6.4.dmg direkt von Apple](https://download.developer.apple.com/Developer_Tools/Xcode_6.4/Xcode_6.4.dmg)
- [Apple-Hinweise zu älteren Xcode-Versionen](https://developer.apple.com/xcode/resources/)

Bei Apple anmelden; laut Apple ist keine kostenpflichtige Developer-Mitgliedschaft
für diese Downloads nötig. Xcode und SDK sind nicht im GitHub-Release enthalten.
Das Diskimage öffnen. Der geprüfte Pfad war `/Volumes/Xcode/Xcode.app`.
Die alte IDE muss für diesen Build nicht gestartet werden. Auf Apple Silicon
müssen die Intel-Werkzeuge ausführbar sein (passende Rosetta-Umgebung).

Prüfen:

```sh
/Volumes/Xcode/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang --version
```

Erwartet: `Apple LLVM version 6.1.0 (clang-602.0.53)`.
Bei abweichendem Speicherort `XCODE_APP` auf den vollständigen Pfad zur
Xcode-6.4-App setzen. Für Build-, Quell- und Toolchainpfade keine Leerzeichen verwenden.

## 2. Projekt und native Python-Version

```sh
git clone https://github.com/Moonklif/appletv3-python39.git
cd appletv3-python39
./scripts/build-host.sh
```

Das lädt die offiziellen CPython-3.9.25-Quellen und prüft SHA-256:

```text
a7438eabd3a48139f42d4e058096af8d880b0bb6e8fb8c78838892e4ce5583f2
```

Der native Interpreter landet unter `work/host/bin/python3.9`. Er läuft auf
dem Mac und erzeugt beim Cross-Build unter anderem Plattform-Konfigurationen.
Der ARMv7-Interpreter kann dafür nicht auf dem Mac ausgeführt werden.
Host-Logs liegen unter `work/host-build/`.

Falls bereits ein funktionierender nativer **CPython 3.9.25** vorliegt, kann
Schritt `build-host.sh` entfallen; dann dessen absoluten Pfad übergeben:

```sh
HOST_PYTHON=/absoluter/pfad/python3.9 ./scripts/build-ios.sh
```

## 3. ARMv7-Build

Mit dem von Schritt 2 erzeugten Host-Python:

```sh
./scripts/build-ios.sh
```

Oder mit anderem Xcode-Speicherort:

```sh
XCODE_APP=/Applications/Xcode_6.4.app ./scripts/build-ios.sh
```

Das Skript prüft die Quellen und wendet die drei Projektpatches
auf `configure`, `configure.ac` und `setup.py` an. Die Ergebnisse sind per
Dateihash an die vorgesehenen Quellversionen gebunden. Unbekannte
Quelländerungen werden abgelehnt; bereits gepatchte Dateien werden übersprungen.
Originale werden als `*.appletv3-original` gesichert. **Autoconf nicht erneut
laufen lassen**: Das passende generierte `configure` wird direkt mitgepatcht.

Die Build-Konfiguration verwendet:

```text
--build=<config.guess des Build-Macs>
--host=arm-apple-darwin
--prefix=/usr/local
--disable-shared
--with-ensurepip=no
-target armv7-apple-ios8.4
-miphoneos-version-min=8.4
```

`config/ios-armv7.site` enthält die vier Cross-Compile-Antworten.
`CC`, `CXX`, `CFLAGS`, `CPPFLAGS` und `LDFLAGS` werden aus Xcode 6.4 und dessen
SDK zusammengesetzt. Es wird kein OpenSSL eingebunden.

Ausgabe: `work/ios-build/python.exe`, eine **Mach-O-Datei für ARMv7**.
Die Endung `.exe` ist das Ergebnis des CPython-Builds auf einem Mac-Dateisystem;
es handelt sich nicht um ein Windows-Programm.

Logs: `work/ios-build/configure.log`, `config.log`, `build.log`.
Bei Fehlern dort nachsehen. `make` kann trotz fehlender optionaler Module
insgesamt erfolgreich enden; die Modulübersicht am Ende von `build.log` prüfen.
Erwartete Einschränkungen: `_ssl`, `_hashlib`, `_lzma` und weitere optionale
Module fehlen, siehe [Prüfstand](BUILD-STATUS.md).

## 4. Installationsarchiv erstellen

```sh
./scripts/package.sh
python3 scripts/inspect-archive.py dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz > dist/rebuilt-archive.json
```

Die Installation wird nach `work/stage/usr/local` umgeleitet. Das Archiv und
seine SHA-256-Datei entstehen in `dist/`. Ein bereits vorhandenes
Staging-Verzeichnis wird nicht überschrieben. Für einen vollständig neuen
Durchlauf ein frisches `WORK` verwenden und es bei allen Schritten gleich setzen.
Optional lässt sich `JOBS=4` für die parallele Kompilierung einstellen.

Das Archiv ist noch **unsigniert**. Weiter mit [Installation und Signierung](INSTALL.md).

## Patchtests

```sh
./scripts/fetch-source.sh
python3 -m unittest discover -s tests -v
```

Die Tests verwenden die tatsächlichen Dateien aus dem offiziellen, per SHA-256
geprüften CPython-Archiv. Sie prüfen exakte Patch-Ergebnisse, Wiederholbarkeit,
Backups und die Ablehnung fremder Änderungen vor der ersten Schreiboperation.
Die GitHub-Prüfung führt diese Tests aus; sie baut weder Xcode noch Apple-TV-Binaries.
