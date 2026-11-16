# HowTo: Python 3.9.25 auf dem Apple TV 3

So baue ich Python auf dem Mac und installiere es auf einem jailbroken
**AppleTV3,2 (A1469)**. Meine getestete Python-Konfiguration verwendet ARMv7 und
Systemversion **8.4.4**. Das SDK- und Compilerziel ist **iOS 8.4**.

Die Schritte sind der Reihe nach gedacht. Jeder Befehlsblock ist mit **Mac**
oder **Apple TV** beschriftet. Wenn das Apple TV bereits jailbroken ist und SSH
funktioniert, Schritt 3 überspringen. Die Mac-Vorbereitung bleibt erforderlich.

## 1. Voraussetzungen

### Mac

- macOS, Internetzugang und ein Administratorkonto für die Werkzeuginstallation.
- Aktuelle Xcode Command Line Tools, Homebrew und Python 3.
- **Xcode 6.4 (6E35b)** mit iPhoneOS-SDK 8.4 für den Python-Cross-Build.
- Auf Apple Silicon eine funktionierende Rosetta-Installation für den alten Intel-Compiler.
- Ein Arbeitsverzeichnis ohne Leerzeichen und ausreichend Platz für Xcode,
  Quellen, zwei Builds und Installationsarchiv. Mit mehreren freien GB planen.

Mein Python-Build wurde auf Apple Silicon geprüft. Blackb0x beschreibt seine
Mac-Unterstützung separat in den [Voraussetzungen](https://github.com/regulad/Blackb0x--#requirements).
Eine dort genannte Mac-Version ist keine zusätzliche Zusage für diesen Python-Port.

### Apple TV und Kabel

- **Apple TV 3 Rev. A, Modell A1469 / AppleTV3,2**; Modellnummer auf dem Gehäuse prüfen.
- Stromkabel und ein **Micro-USB-Datenkabel** für den Jailbreak.
- HDMI und Bildschirm zum Mitlesen; Apple-Remote für die DFU-Anweisungen des Tools.
- Für die folgenden SSH-Befehle müssen Mac und Apple TV im selben Netzwerk sein.
  Die IP-Adresse steht in den Netzwerkeinstellungen des Apple TV oder im Router.

**Firmware prüfen:** Blackb0x und dieser Python-Port haben unterschiedliche
Testumfänge. Vor einem Jailbreak die aktuelle Geräte-/Firmwareunterstützung bei
[Blackb0x--](https://github.com/regulad/Blackb0x--) prüfen. Dessen CLI-Quellstand
vom 16.11.2026 verwendet für AppleTV3,2 den Build `12H1006`; die Bezeichnungen
in README und Quellcode sind nicht durchgehend gleich. Deshalb Modell,
Systemversion und Buildnummer prüfen und kein Update/Restore nur wegen einer
ähnlichen Versionsnummer durchführen. Python wurde hier auf **8.4.4** getestet;
für andere Firmwarestände steht der Laufzeittest noch aus.
[Blackb0x-Zieldefinition](https://github.com/regulad/Blackb0x--/blob/694ab3645ba9fb35457928caffcab77632153a43/src/Cli.cpp#L495).

## 2. Mac-Werkzeuge installieren

**Mac – Terminal:**

```sh
xcode-select --install
```

Installation im macOS-Dialog abschließen. Wenn die Werkzeuge bereits installiert
sind, mit den Prüfungen fortfahren:

```sh
xcode-select -p
clang --version
make --version
git --version
```

[Homebrew nach offizieller Anleitung installieren](https://brew.sh/), falls
`brew --version` noch nicht funktioniert. Die vom Installer angezeigten
„Next steps“ ausführen, damit `brew` im Terminal verfügbar ist.

```sh
brew --version
brew install cmake autoconf automake libtool pkg-config gh python
python3 --version
gh auth login
gh auth status
```

Bei `gh auth login` GitHub.com und die Browser-Anmeldung wählen. Blackb0x nutzt
`gh` zum Laden seiner Firmware-Patches; die Firmware wird aus Apple-Dateien
aufbereitet. Die Python-Skripte benötigen keine GitHub-Anmeldung.

**Nur Apple Silicon, falls Rosetta fehlt – Mac:**

```sh
softwareupdate --install-rosetta
```

Die angezeigten Apple-Hinweise bestätigen. [Apple: Intel-Programme und Rosetta](https://support.apple.com/en-us/102527).

## 3. Apple TV mit Blackb0x vorbereiten

Diesen Schritt überspringen, wenn Jailbreak und SSH bereits funktionieren.
Die folgenden Buildbefehle entsprechen dem
[Blackb0x-Projekt](https://github.com/regulad/Blackb0x--#build).

**Mac:**

```sh
mkdir -p "$HOME/appletv-projects"
cd "$HOME/appletv-projects"
git clone --recurse-submodules https://github.com/regulad/Blackb0x--.git
cd Blackb0x--
cmake -S . -B build
cmake --build build --target jailbreak -j"$(sysctl -n hw.ncpu)"
./build/blackb0x --help
```

Apple TV per Micro-USB mit dem Mac verbinden und mit Strom versorgen. HDMI
bei Bedarf anschließen. Dann **auf dem Mac, ohne `sudo`**, starten:

```sh
./build/blackb0x
```

Den DFU- und Anschlussanweisungen im Terminal folgen. Nach einem fehlgeschlagenen
Exploit das Gerät entsprechend der Tool-Anleitung stromlos machen und erneut
versuchen. Am Ende den von Blackb0x beschriebenen Neustart durchführen.
Sobald der Homescreen wieder erscheint, die Installation der Pakete abwarten.
[Blackb0x-Ablauf](https://github.com/regulad/Blackb0x--#jailbreaking).

Für diesen Weg ist nur das Ziel `jailbreak` vorgesehen. `authoring`, Theos und
`bake-firmware` sind ein eigener Entwicklerweg, falls Blackb0x keine passenden
Firmware-Patches laden kann; dann dessen Fehlermeldung und Dokumentation folgen.

## 4. SSH und Gerätekonfiguration prüfen

**Mac:** Die Beispieladresse durch die tatsächliche Apple-TV-IP ersetzen.
Die Variable gilt für dieses Terminalfenster.

```sh
export ATV_IP="192.168.1.50"
ssh -o HostKeyAlgorithms=+ssh-rsa root@"$ATV_IP"
```

Beim ersten Verbinden den Hostschlüssel des eigenen Geräts prüfen und bestätigen.
Blackb0x nennt `root` und, sofern noch unverändert, das Standardpasswort `alpine`.
Die Option erlaubt den alten RSA-Hostschlüssel nur für diesen Aufruf.
[SSH-Hinweise von Blackb0x](https://github.com/regulad/Blackb0x--/blob/694ab3645ba9fb35457928caffcab77632153a43/scripts/push_authorized_keys.sh).

**Ab jetzt Apple TV – in der SSH-Sitzung:**

```sh
uname -a
sysctl -n hw.machine
cat /System/Library/CoreServices/SystemVersion.plist
id
command -v ldid
command -v tar
df -h
```

Erwartet: `AppleTV3,2`, Root-Rechte und vorhandene Programme `ldid`/`tar`.
`ProductVersion` und `ProductBuildVersion` aus der plist für den eigenen Test
notieren. Wenn `ldid` fehlt, die Blackb0x-Paketinstallation abschließen lassen.
Das Paket ist in dessen [Paketliste](https://github.com/regulad/Blackb0x--/blob/694ab3645ba9fb35457928caffcab77632153a43/package/packages.txt) enthalten.
Bei eingerichtetem Paketmanager lässt es sich auf dem Apple TV nachinstallieren:

```sh
apt-get update
apt-get install ldid
```

Falls noch das Standardpasswort verwendet wird, auf dem Apple TV ändern:

```sh
passwd
```

Zurück zum Mac:

```sh
exit
```

## 5. Xcode 6.4 laden und mounten

**Mac:** Mit dem Apple-Account anmelden und **Xcode 6.4** herunterladen:

- [Apple-Downloadarchiv](https://developer.apple.com/download/all/?q=Xcode%206.4)
- [Xcode_6.4.dmg direkt bei Apple](https://download.developer.apple.com/Developer_Tools/Xcode_6.4/Xcode_6.4.dmg)

Die Datei als `Xcode_6.4.dmg` in Downloads ablegen und öffnen:

```sh
hdiutil attach "$HOME/Downloads/Xcode_6.4.dmg"
export XCODE_APP="/Volumes/Xcode/Xcode.app"
"$XCODE_APP/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang" --version
ls "$XCODE_APP/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"
```

Erwarteter Compiler: `Apple LLVM version 6.1.0 (clang-602.0.53)`. Falls das Image
unter einem anderen Volumenamen gemountet wurde, `XCODE_APP` entsprechend anpassen.
Das Image bis nach der Paketierung gemountet lassen. Die alte Xcode-IDE muss
nicht gestartet werden; die aktive moderne Mac-Toolchain nicht auf Xcode 6.4 umstellen.

## 6. Python-Projekt laden und Host-Python bauen

**Mac:**

```sh
mkdir -p "$HOME/appletv-projects"
cd "$HOME/appletv-projects"
git clone https://github.com/Moonklif/appletv3-python39.git
cd appletv3-python39
./scripts/build-host.sh
./work/host/bin/python3.9 --version
```

Erwartet: `Python 3.9.25`. Das Skript lädt die offiziellen Quellen, prüft ihre
SHA-256 und baut einen **auf dem Mac laufenden** Interpreter. Er wird nur unter
`work/host` installiert. Logs: `work/host-build/`.

## 7. Python für ARMv7 bauen

**Mac – im Verzeichnis `appletv3-python39`:**

```sh
./scripts/build-ios.sh
file work/ios-build/python.exe
```

`XCODE_APP` aus Schritt 5 muss noch gesetzt sein; der Standard ist
`/Volumes/Xcode/Xcode.app`. Das Skript patcht die Quellen und baut mit dem
Host-Python für das Apple TV. Erwartete Dateibeschreibung: **Mach-O executable
arm_v7**. Die Endung `.exe` gehört zum CPython-Build auf dem Mac.

Die Buildausgabe wird in Dateien geschrieben. Bei einem Fehler:

```sh
tail -n 60 work/ios-build/configure.log
tail -n 80 work/ios-build/build.log
```

Fehlende optionale Module wie `_ssl`, `_hashlib` und `_lzma` sind beim aktuellen
Build bekannt. Die vollständige Übersicht steht unter [Build und Tests](BUILD-STATUS.md).

## 8. Installationsarchiv erstellen und prüfen

**Mac:**

```sh
./scripts/package.sh
shasum -a 256 -c dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz.sha256
python3 scripts/inspect-archive.py dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz > dist/rebuilt-archive.json
grep '"extension_count"' dist/rebuilt-archive.json
```

Erwartet: Prüfsumme `OK` und `"extension_count": 63`. Das Archiv liegt unter
`dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz`. Die Dateien werden beim
Paketieren nach `work/stage/usr/local` installiert. Der Mac erhält dadurch
keine ARMv7-Installation in seinem `/usr/local`.

Für einen neuen vollständigen Build ein anderes absolutes `WORK`-Verzeichnis
verwenden und bei allen drei Buildskripten gleich setzen. Das Paketierskript
überschreibt kein bereits vorhandenes `work/stage`.

## 9. Dateien auf das Apple TV übertragen

**Mac – weiterhin im Projektverzeichnis:**

```sh
scp -O -o HostKeyAlgorithms=+ssh-rsa \
  dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz \
  scripts/sign-on-device.sh scripts/smoke-test.py \
  root@"$ATV_IP":/tmp/
ssh -o HostKeyAlgorithms=+ssh-rsa root@"$ATV_IP"
```

`-O` verwendet das klassische SCP-Protokoll, da moderne `scp`-Versionen sonst
SFTP erwarten. Die Verbindung mit dem alten OpenSSH-Server wird so kompatibel
gehalten. Die IP-Variable aus Schritt 4 muss im Mac-Terminal noch gesetzt sein.

## 10. Sichern, installieren und signieren

**Apple TV – in der SSH-Sitzung, als `root`:**

```sh
df -h
if [ -d /usr/local ]; then
  tar -czf "/var/root/usr-local-before-python39-$(date +%Y%m%d-%H%M%S).tar.gz" -C / usr/local
fi
```

Nur bei erfolgreicher Sicherung und genügend freiem Platz fortfahren. Das
Archiv enthält `usr/local/…`; die Extraktion ersetzt dort gleichnamige Dateien.

```sh
tar -xzf /tmp/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz -C /
sh /tmp/sign-on-device.sh
/usr/local/bin/python3.9 --version
```

Erwartet: `Python 3.9.25`. Das Skript führt `ldid -S` für den Interpreter und
jedes `.so` in `lib-dynload` aus. **Diese Befehle auf dem Apple TV ausführen.**

## 11. Python testen

**Apple TV:**

```sh
/usr/local/bin/python3.9 /tmp/smoke-test.py
```

Der Test prüft die Imports und einen kurz laufenden HTTP-Server auf Loopback.
Die letzte Erfolgsmeldung lautet:

```text
PASS loopback HTTP 200
```

Eigener Kurztest:

```sh
/usr/local/bin/python3.9 -c 'import sys, sqlite3; print(sys.version); print("SQLite", sqlite3.sqlite_version)'
```

Damit ist Python installiert. `ssl`, `lzma` und `ctypes` sind in diesem Build
nicht verfügbar; ein funktionierendes System-TLS von Blackb0x ändert das nicht.

## Häufige Probleme

| Meldung | Nächster Schritt |
| --- | --- |
| `brew: command not found` | Homebrew-Installation und deren „Next steps“ abschließen. |
| `Bad CPU type in executable` beim alten clang | Auf Apple Silicon Rosetta und die Ausführbarkeit von Xcode 6.4 prüfen. |
| SSH: `Connection refused` | IP, Netzwerk und abgeschlossene Blackb0x-/OpenSSH-Installation prüfen. |
| SSH: kein passender Hostschlüssel | Die oben gezeigte Option `HostKeyAlgorithms=+ssh-rsa` verwenden. |
| SCP meldet fehlendes SFTP | `scp -O` wie oben verwenden. |
| `ldid: not found` auf dem Apple TV | Blackb0x-Pakete fertig installieren oder `ldid` mit dem Geräte-Paketmanager installieren. |
| Python endet mit `Killed: 9` | Interpreter und Erweiterungen erneut mit dem Signierskript signieren. |
| `Stage already exists` | Für einen neuen Build ein frisches `WORK` verwenden. |
| `Read-only file system` beim Installieren | Jailbreak und Schreibzugriff auf dem Gerät prüfen, bevor weiter installiert wird. |

### Quellen

- [Blackb0x--: Projekt und aktuelle Anleitung](https://github.com/regulad/Blackb0x--), abgeglichen mit Commit `694ab3645ba9fb35457928caffcab77632153a43` am 16.11.2026.
- [Apple: Command Line Tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools).
- [Homebrew: Installation](https://docs.brew.sh/Installation).
- [Apple: ältere Xcode-Versionen](https://developer.apple.com/xcode/resources/).
- [OpenSSH: scp, Option `-O`](https://man.openbsd.org/scp#O).
