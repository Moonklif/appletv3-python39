#!/bin/sh
# Run on the jailbroken Apple TV after installing into /usr/local.
set -eu
command -v ldid >/dev/null
ldid -S /usr/local/bin/python3.9
find /usr/local/lib/python3.9/lib-dynload -name '*.so' -type f -exec ldid -S {} \;
/usr/local/bin/python3.9 --version
