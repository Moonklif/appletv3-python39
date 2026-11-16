#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
WORK=${WORK:-"$ROOT/work"}
mkdir -p "$WORK"
ARCHIVE="$WORK/Python-3.9.25.tgz"
if [[ ! -f "$ARCHIVE" ]]; then
    curl --fail --location --output "$ARCHIVE" https://www.python.org/ftp/python/3.9.25/Python-3.9.25.tgz
fi
printf '%s  %s\n' a7438eabd3a48139f42d4e058096af8d880b0bb6e8fb8c78838892e4ce5583f2 "$ARCHIVE" | shasum -a 256 -c -
if [[ ! -d "$WORK/Python-3.9.25" ]]; then
    tar -xzf "$ARCHIVE" -C "$WORK"
fi
printf 'Source: %s\n' "$WORK/Python-3.9.25"
