# CPython 3.9.25 for Apple TV 3

## Deutsch

### Ziel

Dieses Repository dokumentiert die Arbeit an einem CPython-3.9.25-Build für
Apple TV 3. Generation. Der bisher bestätigte Zielumfang ist:

- Gerät: AppleTV3,2
- Architektur: ARMv7
- Betriebssystem: Apple TV Software 8.4.4

### Dokumentationsumfang

Der vorgesehene Ablauf umfasst die Erstellung des CPython-Builds, einen
projektspezifischen `setup.py`-Patch, die Installation auf dem Gerät, die
Signierung mit `ldid` und einen HTTP-Server-Test. Die konkreten Build-Befehle,
der Inhalt des Patches, Installationspfade und Testergebnisse sind im derzeit
geprüften Repository-Stand nicht vorhanden. Sie werden daher hier nicht
rekonstruiert oder als funktionierend dargestellt.

### Wichtige Einschränkungen

- Es ist kein tatsächlich erzeugtes oder geprüftes Binärpaket veröffentlicht.
- SSL/TLS- beziehungsweise OpenSSL-Unterstützung ist nicht bestätigt. Diese
  Funktionen dürfen weder vorausgesetzt noch als verfügbar dokumentiert werden.
- Weitere Abhängigkeiten, Build-Werkzeuge, SDK-Versionen, Konfigurationsoptionen
  und Laufzeitvoraussetzungen sind nicht bestätigt.
- Ohne den tatsächlich geprüften `setup.py`-Patch darf kein Patchtext oder
  Patch-Befehl angegeben werden.
- Ohne einen verifizierten Lauf darf weder eine erfolgreiche `ldid`-Signierung
  noch ein erfolgreicher HTTP-Server-Test behauptet werden.

### Nächster dokumentierbarer Stand

Sobald Quellstand, Build-Umgebung, exakter Patch und Testausgaben geprüft
vorliegen, kann diese README um reproduzierbare Befehle und deren Ergebnisse
ergänzt werden. Bis dahin bleibt sie bewusst eine Bestands- und
Einschränkungsdokumentation.

## English

### Target

This repository documents work on a CPython 3.9.25 build for the third-
generation Apple TV. The confirmed target scope is:

- Device: AppleTV3,2
- Architecture: ARMv7
- Operating system: Apple TV Software 8.4.4

### Documentation scope

The intended workflow covers building CPython, applying a project-specific
`setup.py` patch, installing the result on the device, signing with `ldid`, and
testing an HTTP server. Concrete build commands, the patch contents,
installation paths, and test results are not present in the currently reviewed
repository state. They are therefore not reconstructed here or presented as
working.

### Important limitations

- No generated or verified binary package is published.
- SSL/TLS and OpenSSL support are unconfirmed. They must not be assumed or
  documented as available.
- Other dependencies, build tools, SDK versions, configuration options, and
  runtime requirements are unconfirmed.
- No patch text or patch command is provided without the verified `setup.py`
  patch.
- No successful `ldid` signing or HTTP-server test is claimed without a
  verified run.

### Next documentable state

Once the source revision, build environment, exact patch, and test output have
been verified, this README can be extended with reproducible commands and their
results. Until then, it intentionally remains an inventory and limitations
document.
