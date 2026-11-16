# Build on macOS

Target: a jailbroken **AppleTV3,2**, Apple TV Software **8.4.4**. The compiler
and SDK target is **iOS 8.4**, not `8.4.4`. These commands run on the Mac;
packaging stages files locally instead of installing ARMv7 files into the Mac's
`/usr/local`.

## Requirements

Use current Mac developer tools for a native CPython 3.9.25 host interpreter,
and a separate **Xcode 6.4 (6E35b), iOS SDK 8.4, Apple LLVM 6.1.0
(clang-602.0.53)** for the target build. This exact target toolchain was found
on the original machine and used for the fresh cross-build.

- [Apple's Xcode 6.4 download search](https://developer.apple.com/download/all/?q=Xcode%206.4)
- [Apple's Xcode_6.4.dmg download](https://download.developer.apple.com/Developer_Tools/Xcode_6.4/Xcode_6.4.dmg)
- [Apple's older Xcode download information](https://developer.apple.com/xcode/resources/)

Sign in with an Apple Account. Apple says paid Developer Program membership is
not required for these downloads. Xcode and the SDK are obtained from Apple;
they are not bundled here. Mount the disk image. The verified location was
`/Volumes/Xcode/Xcode.app`. You do not need to launch the old IDE. On Apple
Silicon, the Intel toolchain must be executable (a suitable Rosetta setup).
A current Xcode does not replace this old ARMv7 target toolchain.

```sh
/Volumes/Xcode/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang --version
```

Expect `Apple LLVM version 6.1.0 (clang-602.0.53)`. Set `XCODE_APP` to the full
path to your Xcode 6.4 app if it is elsewhere. Use build, source, interpreter
and toolchain paths without spaces.

## Build a native host interpreter

```sh
git clone https://github.com/Moonklif/appletv3-python39.git
cd appletv3-python39
./scripts/build-host.sh
```

The source comes from the official Python download and is checked against:

```text
a7438eabd3a48139f42d4e058096af8d880b0bb6e8fb8c78838892e4ce5583f2
```

The native interpreter is installed under `work/host/bin/python3.9`; logs are
in `work/host-build/`. It runs on the Mac and generates cross-build metadata.
An ARMv7 interpreter cannot perform that job on the Mac.

If you already have a working native **CPython 3.9.25**, skip `build-host.sh`
and use its absolute path:

```sh
HOST_PYTHON=/absolute/path/python3.9 ./scripts/build-ios.sh
```

## Build the target interpreter

With the host Python built above:

```sh
./scripts/build-ios.sh
```

For a different Xcode location:

```sh
XCODE_APP=/Applications/Xcode_6.4.app ./scripts/build-ios.sh
```

The script applies recovered patches to `configure`, `configure.ac` and
`setup.py`. File hashes enforce exact original or already-patched contents.
Unknown edits are rejected. Original files are backed up as
`*.appletv3-original`. **Do not regenerate configure with Autoconf**: both the
input and the matching generated shell script are patched directly.

The reconstructed settings are:

```text
--build=<build Mac's config.guess result>
--host=arm-apple-darwin
--prefix=/usr/local
--disable-shared
--with-ensurepip=no
-target armv7-apple-ios8.4
-miphoneos-version-min=8.4
```

`config/ios-armv7.site` contains the four recovered configure answers. The
compiler and flags reference Xcode 6.4 and its SDK. OpenSSL is not supplied.

Output: `work/ios-build/python.exe`, a **Mach-O ARMv7 executable**. The `.exe`
suffix comes from CPython's build on the Mac filesystem; it is not Windows code.
Logs: `work/ios-build/configure.log`, `config.log`, `build.log`.
Check the optional-module summary even if `make` succeeds. `_ssl`, `_hashlib`,
`_lzma` and some other optional modules are absent; see [build status](BUILD-STATUS.md).

## Package

```sh
./scripts/package.sh
python3 scripts/inspect-archive.py dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz > dist/rebuilt-archive.json
```

Files are installed into `work/stage/usr/local`. The archive and its SHA-256
file are written to `dist/`. Existing staging directories are refused. For a
clean repeat, choose a fresh absolute `WORK` path and use it consistently for
all scripts. `JOBS` controls compilation parallelism and defaults to 4.

The archive is **unsigned**. Continue with [installation and signing](INSTALL.md).

## Verify the patches

```sh
./scripts/fetch-source.sh
python3 -m unittest discover -s tests -v
```

The tests use actual checksum-verified upstream files. They check exact output,
repeat application, backups, and rejection of unknown changes before mutation.
GitHub checks run these tests, not an Xcode or Apple TV binary build.
