#!/bin/bash
# Build a native 3.9.25 interpreter using the current Mac toolchain.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
export WORK=${WORK:-"$ROOT/work"}
"$ROOT/scripts/fetch-source.sh"
# Keep native sources separate from the patched target sources.
if [[ ! -d "$WORK/host-source/Python-3.9.25" ]]; then
    mkdir -p "$WORK/host-source"
    tar -xzf "$WORK/Python-3.9.25.tgz" -C "$WORK/host-source"
fi
mkdir -p "$WORK/host-build"
cd "$WORK/host-build"
"$WORK/host-source/Python-3.9.25/configure" --prefix="$WORK/host" --with-ensurepip=no > configure.log 2>&1
make -j "${JOBS:-4}" > build.log 2>&1
make install > install.log 2>&1
"$WORK/host/bin/python3.9" --version
