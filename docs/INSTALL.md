# Installation, signing and runtime checks / Installation und Laufzeittests

## Deutsch

Voraussetzung: bereits jailbroken **AppleTV3,2**, Firmware **8.4.4**, Shell-Zugang
mit Schreibrechten für `/usr/local` und ein funktionierendes `ldid` auf dem
Gerät. Jailbreak und Bereitstellung von `ldid` sind nicht Teil dieses Projekts.

1. Archiv aus den [Releases](https://github.com/Moonklif/appletv3-python39/releases)
   herunterladen oder [selbst bauen](BUILD-DE.md). Das Originalarchiv und der
   neue Build sind getrennt benannt. Beide sind unsigniert.
2. Auf dem Mac den Download gegen `SHA256SUMS` des Releases prüfen:

   ```sh
   shasum -a 256 -c SHA256SUMS
   ```

   Für den vollständigen Prüflauf alle dort aufgeführten Dateien herunterladen;
   fehlende Dateien werden vom Prüfwerkzeug gemeldet. Ein lokaler Neubau hat
   seine eigene `.sha256`-Datei; deren Dateipfad gegebenenfalls anpassen.
3. Archiv sowie `scripts/sign-on-device.sh` und `scripts/smoke-test.py` aus dem
   Repository auf das Apple TV übertragen, zum Beispiel per `scp` nach `/tmp/`.
   Zieladresse und Anmeldung hängen vom eigenen Gerät ab.
4. Vorhandene Python-Dateien unter `/usr/local` vorher sichern. Das Archiv enthält
   `usr/local/…`; die folgende Extraktion installiert/überschreibt Dateien dort.
   **Ab hier auf dem Apple TV ausführen**, als Benutzer mit ausreichenden Rechten:

   ```sh
   tar -xzf /tmp/AppleTV3-Python39-armv7-8.4.4.tar.gz -C /
   sh /tmp/sign-on-device.sh
   /usr/local/bin/python3.9 /tmp/smoke-test.py
   ```

   Für den Neubau den Dateinamen durch
   `AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz` ersetzen.

Die Signierung entspricht dem historischen Vorgehen: `ldid -S` für den
Interpreter und jedes `.so` in `lib-dynload`. Bei `Killed: 9` zuerst die
Signierung des Interpreters prüfen. Die historische erfolgreiche Version war
`Python 3.9.25`.

Der neue Smoke-Test prüft die dokumentierten Imports und einen temporären
HTTP-Server auf Loopback. Er öffnet keinen öffentlich erreichbaren Webserver.
Der frühere manuelle HTTP-Test nutzte `127.0.0.1:18080`; der neue Test verwendet
einen freien Port. Erfolgsanzeige: `PASS loopback HTTP 200`.

SSL/TLS ist in diesen Paketen nicht enthalten. Ein Import von `ssl`, `lzma`
oder `ctypes` kann trotz vorhandener Python-Wrapper fehlschlagen, weil die
native Erweiterung fehlt. Es gibt keine neue Geräteprüfung dieser Release-Pakete;
die dokumentierten Gerätetests stammen aus dem ursprünglichen Arbeitsverlauf.

## English

Requires an already jailbroken **AppleTV3,2** running **8.4.4**, shell access
with permission to write `/usr/local`, and working `ldid` on the device.
Jailbreaking and provisioning `ldid` are outside this project.

1. Download an archive from [Releases](https://github.com/Moonklif/appletv3-python39/releases)
   or [build it](BUILD-EN.md). The original and rebuilt archives have distinct
   filenames; both are unsigned.
2. Verify downloads on the Mac using `shasum -a 256 -c SHA256SUMS`. Download all
   listed files for a complete pass; missing files are reported. A local rebuild
   has its own `.sha256` file, whose pathname may need adjustment.
3. Transfer the archive, `scripts/sign-on-device.sh`, and `scripts/smoke-test.py`
   to the Apple TV, for example using `scp` into `/tmp/`, with your own device
   address and login.
4. Back up existing Python files under `/usr/local`. Extraction installs or
   replaces files there. **Run on the Apple TV**, with sufficient permissions:

   ```sh
   tar -xzf /tmp/AppleTV3-Python39-armv7-8.4.4.tar.gz -C /
   sh /tmp/sign-on-device.sh
   /usr/local/bin/python3.9 /tmp/smoke-test.py
   ```

   Substitute `AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz` for the new build.

The signing script runs `ldid -S` on the interpreter and each extension module,
matching the historical procedure. If you get `Killed: 9`, check interpreter
signing first. The expected version is `Python 3.9.25`.

The new smoke test checks imports and starts a temporary loopback HTTP server
on an available port. The historical manual HTTP check used port 18080.
Expected final output: `PASS loopback HTTP 200`.

SSL/TLS is absent. Imports of `ssl`, `lzma` or `ctypes` can fail because their
native extension is missing, even though Python wrapper files are present.
These release packages have not received a new device runtime test; recorded
device results come from the original work history.
