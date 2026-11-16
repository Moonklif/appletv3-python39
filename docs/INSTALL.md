# Installation und Tests / Installation and tests

## Deutsch

Für die Vorbereitung von Mac und Apple TV sowie alle Schritte ab dem Jailbreak
siehe [HowTo](HOWTO-DE.md). Diese Kurzfassung setzt ein jailbroken AppleTV3,2,
Root-SSH und `ldid` voraus.

### 1. Archiv wählen

Entweder [selbst bauen](BUILD-DE.md) oder aus den
[Releases](https://github.com/Moonklif/appletv3-python39/releases) laden.
`AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz` ist der mit den Buildskripten
erzeugte Build. Beide angebotenen Binärarchive sind unsigniert.

Für einen Release-Download die Prüfsumme aus `SHA256SUMS` prüfen. Werden alle
dort aufgeführten Dateien geladen, lautet der Befehl auf dem Mac:

```sh
shasum -a 256 -c SHA256SUMS
```

### 2. Übertragen – Mac

Im Repository-Verzeichnis, IP-Adresse anpassen:

```sh
export ATV_IP="192.168.1.50"
scp -O -o HostKeyAlgorithms=+ssh-rsa \
  dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz \
  scripts/sign-on-device.sh scripts/smoke-test.py \
  root@"$ATV_IP":/tmp/
ssh -o HostKeyAlgorithms=+ssh-rsa root@"$ATV_IP"
```

Bei einem Release-Download statt `dist/…` dessen lokalen Dateipfad einsetzen.
`-O` nutzt klassisches SCP für den alten Server. Den Hostschlüssel des eigenen
Geräts beim ersten Verbinden prüfen.

### 3. Sichern und installieren – Apple TV, als root

```sh
df -h
if [ -d /usr/local ]; then
  tar -czf "/var/root/usr-local-before-python39-$(date +%Y%m%d-%H%M%S).tar.gz" -C / usr/local
fi
```

Nach erfolgreicher Sicherung und bei ausreichend freiem Platz:

```sh
tar -xzf /tmp/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz -C /
sh /tmp/sign-on-device.sh
/usr/local/bin/python3.9 --version
/usr/local/bin/python3.9 /tmp/smoke-test.py
```

Die Extraktion ersetzt gleichnamige Dateien unter `/usr/local`. Bei Verwendung
des Basisarchivs den Dateinamen ohne `-rebuilt` einsetzen.
Erwartet: `Python 3.9.25` und `PASS loopback HTTP 200`.

Das Signierskript führt `ldid -S` für den Interpreter und alle `.so`-Module aus.
Bei `Killed: 9` zuerst diese Signierung prüfen. Der Smoke-Test prüft Imports
und einen temporären lokalen HTTP-Server. SSL/TLS, LZMA und ctypes fehlen;
siehe [Build und Tests](BUILD-STATUS.md).

## English

Start with the [HowTo](HOWTO-EN.md) for Mac/device setup and jailbreaking.
This short path assumes a jailbroken AppleTV3,2, root SSH and `ldid`.

Build the archive using [the build guide](BUILD-EN.md) or download it from
[Releases](https://github.com/Moonklif/appletv3-python39/releases). Verify the
release downloads with `shasum -a 256 -c SHA256SUMS` when all listed files are
present. Both binary archives are unsigned.

Use the Mac transfer commands above, replacing `ATV_IP` and the local archive
path. `scp -O` supports the old server. Check its host key on first connection.
On Apple TV as root, check free space and back up `/usr/local` using the backup
block above. Continue only after a successful backup. Then extract the archive,
run `sign-on-device.sh`, check the version and run `smoke-test.py` with the
commands above. Extraction replaces matching `/usr/local` files.

Expected output: `Python 3.9.25` and `PASS loopback HTTP 200`. Signing covers
the interpreter and all native extensions. SSL/TLS, LZMA and ctypes are absent;
see [build and tests](BUILD-STATUS.md).
