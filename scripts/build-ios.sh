#!/bin/bash
# Cross-compile CPython 3.9.25 with Xcode 6.4 for Apple TV 3 ARMv7.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
export WORK=${WORK:-"$ROOT/work"}
XCODE_APP=${XCODE_APP:-/Volumes/Xcode/Xcode.app}
SDK="$XCODE_APP/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"
TOOLBIN="$XCODE_APP/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin"
HOST_PYTHON=${HOST_PYTHON:-"$WORK/host/bin/python3.9"}
[[ $(uname -s) == Darwin ]] || { echo 'macOS is required.' >&2; exit 1; }
[[ -x "$TOOLBIN/clang" && -d "$SDK" ]] || { echo 'Mount Xcode_6.4.dmg or set XCODE_APP to Xcode 6.4.' >&2; exit 1; }
# CPython 3.9 make rules and embedded compiler commands need paths without spaces.
case "$WORK:$XCODE_APP:$HOST_PYTHON" in *' '*) echo 'Use paths without spaces for WORK, XCODE_APP and HOST_PYTHON.' >&2; exit 1;; esac
[[ "$HOST_PYTHON" = /* ]] || { echo 'HOST_PYTHON must be an absolute path.' >&2; exit 1; }
[[ $("$HOST_PYTHON" -c 'import sys; print(".".join(map(str,sys.version_info[:3])))') == 3.9.25 ]] || { echo 'Native CPython 3.9.25 is required.' >&2; exit 1; }
"$ROOT/scripts/fetch-source.sh"
SRC="$WORK/Python-3.9.25"
python3 "$ROOT/scripts/apply-patches.py" "$SRC"
mkdir -p "$WORK/host-bin" "$WORK/ios-build"
ln -sf "$HOST_PYTHON" "$WORK/host-bin/python3.9"
export PATH="$WORK/host-bin:$PATH"
export CONFIG_SITE="$ROOT/config/ios-armv7.site"
export CC="$TOOLBIN/clang -target armv7-apple-ios8.4 -isysroot $SDK -miphoneos-version-min=8.4"
export CXX="$TOOLBIN/clang++ -target armv7-apple-ios8.4 -isysroot $SDK -miphoneos-version-min=8.4"
export CFLAGS="-O2 -target armv7-apple-ios8.4 -isysroot $SDK -miphoneos-version-min=8.4"
export CPPFLAGS="-isysroot $SDK"
export LDFLAGS="-isysroot $SDK -miphoneos-version-min=8.4"
# Prevent unrelated local Python settings from contaminating the cross build.
unset PYTHONHOME PYTHONPATH _PYTHON_HOST_PLATFORM _PYTHON_SYSCONFIGDATA_NAME
cd "$WORK/ios-build"
"$SRC/configure" --build="$(/bin/sh "$SRC/config.guess")" --host=arm-apple-darwin \
    --prefix=/usr/local --disable-shared --with-ensurepip=no > configure.log 2>&1
make -j "${JOBS:-4}" > build.log 2>&1
file python.exe
printf 'Build logs: %s\n' "$WORK/ios-build"
