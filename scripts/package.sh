#!/bin/bash
# Stage files locally; this never installs target files onto the build Mac.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
WORK=${WORK:-"$ROOT/work"}
STAGE="$WORK/stage"
[[ ! -e "$STAGE" ]] || { echo 'Stage already exists. Use a fresh WORK directory or move stage aside.' >&2; exit 1; }
mkdir -p "$STAGE" "$ROOT/dist"
export PATH="$WORK/host-bin:$PATH"
unset PYTHONHOME PYTHONPATH _PYTHON_HOST_PLATFORM _PYTHON_SYSCONFIGDATA_NAME
cd "$WORK/ios-build"
make install DESTDIR="$STAGE" > package-install.log 2>&1
# Include CPython and bundled-component notices in the install tree.
cp "$ROOT/LICENSES/CPython-3.9.25.txt" "$STAGE/usr/local/lib/python3.9/LICENSE.txt"
# Do not ship build-machine bytecode caches.
find "$STAGE" -name __pycache__ -type d -prune -exec rm -rf {} +
ARCHIVE="$ROOT/dist/AppleTV3-Python39-armv7-8.4.4-rebuilt.tar.gz"
COPYFILE_DISABLE=1 tar -czf "$ARCHIVE" -C "$STAGE" usr/local
shasum -a 256 "$ARCHIVE" > "$ARCHIVE.sha256"
printf 'Unsigned target archive: %s\n' "$ARCHIVE"
