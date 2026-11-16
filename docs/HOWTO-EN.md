# HowTo: Python 3.9.25 on Apple TV 3

This is how I build Python on a Mac and install it on a jailbroken
**AppleTV3,2 (A1469)**. My tested configuration is ARMv7, system version
**8.4.4**, with compiler/SDK target **iOS 8.4**.

Follow the steps in order. Blocks are labelled **Mac** or **Apple TV**.
If the device is already jailbroken and SSH works, skip step 3. The Mac setup
is still required.

## 1. Requirements

**Mac:** macOS, internet access, an administrator account for tool installation,
current Command Line Tools, Homebrew, Python 3, **Xcode 6.4 (6E35b) / iOS SDK
8.4**, and working Rosetta on Apple Silicon for the Intel compiler. Use paths
without spaces and allow several GB for tools, sources, builds and packaging.
My Python build was checked on Apple Silicon. Blackb0x lists its own
[Mac requirements](https://github.com/regulad/Blackb0x--#requirements); those do
not extend this Python port's tested configurations.

**Apple TV:** third-generation Rev. A, **A1469 / AppleTV3,2**, power cable,
Micro-USB **data** cable for jailbreaking, and optionally HDMI/a display to
follow progress. Have the Apple Remote ready for the tool's DFU instructions.
For the SSH commands below, put the Mac and Apple TV on the same network and
find the device's IP in its network settings or your router.

**Check firmware before jailbreaking.** Blackb0x support and this Python port's
tested configuration are separate. The Blackb0x CLI checked on 2026-11-16 uses
build `12H1006` for AppleTV3,2; version labels in its README and source are not
fully consistent. Check model, system version and build ID instead of updating
or restoring based on a similar version number. Python here was tested on
**8.4.4**; runtime tests on other firmware are pending.
[Blackb0x target definition](https://github.com/regulad/Blackb0x--/blob/694ab3645ba9fb35457928caffcab77632153a43/src/Cli.cpp#L495).

## 2. Set up the Mac tools

**Mac – Terminal:**

```sh
xcode-select --install
```

Complete the macOS dialog, or continue if the tools are already installed:

```sh
xcode-select -p
clang --version
make --version
git --version
```

Install Homebrew using its [official instructions](https://brew.sh/) if needed.
Complete the installer's “Next steps” so `brew` works in the terminal.

```sh
brew --version
brew install cmake autoconf automake libtool pkg-config gh python
python3 --version
gh auth login
gh auth status
```

Choose GitHub.com and browser authentication. Blackb0x uses `gh` to obtain its
firmware patches; the Python scripts do not require GitHub authentication.

**Apple Silicon only, if Rosetta is missing – Mac:**

```sh
softwareupdate --install-rosetta
```

Review Apple's prompts. [Apple's Rosetta guide](https://support.apple.com/en-us/102527).

## 3. Jailbreak using Blackb0x

Skip this step if jailbreaking and SSH are already working. Based on the
[upstream build instructions](https://github.com/regulad/Blackb0x--#build).

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

Connect the Apple TV using Micro-USB and power, plus HDMI if desired.
Run **on the Mac without `sudo`**:

```sh
./build/blackb0x
```

Follow its terminal instructions for DFU and cables. If the exploit fails,
follow its power-cycle/retry instructions. Complete the restart described by
the tool and let package installation finish after the home screen returns.
[Upstream jailbreak procedure](https://github.com/regulad/Blackb0x--#jailbreaking).

This path builds only `jailbreak`. If suitable firmware patches cannot be
obtained, follow the upstream error and documentation for its separate
`authoring`/Theos/`bake-firmware` workflow.

## 4. Connect over SSH and check the device

**Mac:** replace this example address with the Apple TV's IP. Keep this
terminal open; the variable is used again later.

```sh
export ATV_IP="192.168.1.50"
ssh -o HostKeyAlgorithms=+ssh-rsa root@"$ATV_IP"
```

Check and accept your device's host key on the first connection. Blackb0x uses
`root`; the unchanged default password is `alpine`. The option permits the
legacy RSA host key only for this invocation.
[Upstream SSH notes](https://github.com/regulad/Blackb0x--/blob/694ab3645ba9fb35457928caffcab77632153a43/scripts/push_authorized_keys.sh).

**Apple TV – inside SSH:**

```sh
uname -a
sysctl -n hw.machine
cat /System/Library/CoreServices/SystemVersion.plist
id
command -v ldid
command -v tar
df -h
```

Expect `AppleTV3,2`, root permissions, `ldid` and `tar`. Record `ProductVersion`
and `ProductBuildVersion` from the plist. If `ldid` is absent, let Blackb0x's
package installation finish; it is in the upstream
[package list](https://github.com/regulad/Blackb0x--/blob/694ab3645ba9fb35457928caffcab77632153a43/package/packages.txt).
With a working package manager, install it **on the Apple TV**:

```sh
apt-get update
apt-get install ldid
```

If still using the default password, change it on the device:

```sh
passwd
```

Return to the Mac:

```sh
exit
```

## 5. Download and mount Xcode 6.4

**Mac:** sign in with an Apple Account and download **Xcode 6.4**:
[Apple download archive](https://developer.apple.com/download/all/?q=Xcode%206.4) ·
[Apple's Xcode_6.4.dmg](https://download.developer.apple.com/Developer_Tools/Xcode_6.4/Xcode_6.4.dmg).
Save it to Downloads as `Xcode_6.4.dmg`.

```sh
hdiutil attach "$HOME/Downloads/Xcode_6.4.dmg"
export XCODE_APP="/Volumes/Xcode/Xcode.app"
"$XCODE_APP/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang" --version
ls "$XCODE_APP/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"
```

Expect `Apple LLVM version 6.1.0 (clang-602.0.53)`. Adjust `XCODE_APP` if the
mount name differs. Keep the image mounted until packaging finishes. You do
not need to launch the old IDE or switch the active modern Mac toolchain to it.

## 6. Clone the Python project and build host Python

**Mac:**

```sh
mkdir -p "$HOME/appletv-projects"
cd "$HOME/appletv-projects"
git clone https://github.com/Moonklif/appletv3-python39.git
cd appletv3-python39
./scripts/build-host.sh
./work/host/bin/python3.9 --version
```

Expect `Python 3.9.25`. The script downloads checksum-verified official sources
and builds a **native Mac interpreter**, installed only into `work/host`.
Logs: `work/host-build/`.

## 7. Build ARMv7 Python

**Mac – inside `appletv3-python39`:**

```sh
./scripts/build-ios.sh
file work/ios-build/python.exe
```

Keep `XCODE_APP` from step 5 set; the default is `/Volumes/Xcode/Xcode.app`.
The script patches the sources and uses host Python to build for Apple TV.
Expect **Mach-O executable arm_v7**. The `.exe` suffix comes from CPython's
build on the Mac.

If the script fails, inspect its logs:

```sh
tail -n 60 work/ios-build/configure.log
tail -n 80 work/ios-build/build.log
```

Missing optional `_ssl`, `_hashlib` and `_lzma` modules are expected for the
current build. See [build and tests](BUILD-STATUS.md).

## 8. Package and verify

**Mac:**

```sh
./scripts/package.sh
shasum -a 256 -c dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz.sha256
python3 scripts/inspect-archive.py dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz > dist/rebuilt-archive.json
grep '"extension_count"' dist/rebuilt-archive.json
```

Expect checksum `OK` and `"extension_count": 63`. The archive is in `dist/`.
Installation is staged into `work/stage/usr/local`; ARMv7 files are not installed
into the Mac's `/usr/local`. For a complete repeat, use a new absolute `WORK`
path consistently across all three build scripts. Existing staging directories
are refused.

## 9. Transfer to Apple TV

**Mac – still inside the project:**

```sh
scp -O -o HostKeyAlgorithms=+ssh-rsa \
  dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz \
  scripts/sign-on-device.sh scripts/smoke-test.py \
  root@"$ATV_IP":/tmp/
ssh -o HostKeyAlgorithms=+ssh-rsa root@"$ATV_IP"
```

`-O` selects classic SCP for compatibility with the old server rather than
modern scp's SFTP default. Keep `ATV_IP` set in the Mac terminal.

## 10. Back up, install and sign

**Apple TV – inside SSH as root:**

```sh
df -h
if [ -d /usr/local ]; then
  tar -czf "/var/root/usr-local-before-python39-$(date +%Y%m%d-%H%M%S).tar.gz" -C / usr/local
fi
```

Continue only after a successful backup and with enough free space.
Extraction replaces matching files under `/usr/local`.

```sh
tar -xzf /tmp/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz -C /
sh /tmp/sign-on-device.sh
/usr/local/bin/python3.9 --version
```

Expect `Python 3.9.25`. The script signs the interpreter and every extension
using `ldid -S`. **Run these commands on Apple TV.**

## 11. Test Python

**Apple TV:**

```sh
/usr/local/bin/python3.9 /tmp/smoke-test.py
/usr/local/bin/python3.9 -c 'import sys, sqlite3; print(sys.version); print("SQLite", sqlite3.sqlite_version)'
```

The smoke test checks imports and temporary loopback HTTP. Its final success
message is `PASS loopback HTTP 200`. SSL/TLS, LZMA and ctypes are unavailable
in this Python build, even if Blackb0x provides system TLS.

## Troubleshooting

| Message | Check |
| --- | --- |
| `brew: command not found` | Complete Homebrew's installation and “Next steps”. |
| Old clang: `Bad CPU type in executable` | Check Rosetta and execution of the Intel compiler on Apple Silicon. |
| SSH: connection refused | Check IP, network and completion of Blackb0x/OpenSSH setup. |
| SSH: no matching host key | Use the command-local `HostKeyAlgorithms=+ssh-rsa` option shown above. |
| SCP: missing SFTP | Use `scp -O`. |
| Missing `ldid` | Complete Blackb0x packages or install `ldid` through the device package manager. |
| Python: `Killed: 9` | Run the signing script again for the interpreter and extensions. |
| `Stage already exists` | Use a fresh `WORK` for another build. |
| Read-only filesystem | Check jailbreak status and write access before installation. |

Sources: [Blackb0x--](https://github.com/regulad/Blackb0x--) (checked against
commit `694ab3645ba9fb35457928caffcab77632153a43` on 2026-11-16),
[Apple Command Line Tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools),
[Homebrew installation](https://docs.brew.sh/Installation),
[Apple older Xcode downloads](https://developer.apple.com/xcode/resources/),
[OpenSSH scp `-O`](https://man.openbsd.org/scp#O).
