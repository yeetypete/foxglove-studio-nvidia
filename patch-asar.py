#!/usr/bin/env python3
"""Enable NVDEC video decode in Foxglove Studio by patching app.asar.

Chromium disables VA-API on NVIDIA unless the VaapiOnNvidiaGPUs feature is on.
Foxglove sets its own --enable-features list via app.commandLine.appendSwitch,
which discards any list passed on the command line, so the only way to enable
the feature is to add it to the list hard-coded in app.asar (original kept
as app.asar.orig).
(Tested on Foxglove 3.0.0 / Electron 43 / Chromium 150.)
"""

import argparse
import shutil
import sys
from pathlib import Path

DEFAULT_ASAR = Path("/opt/Foxglove/resources/app.asar")
OLD = b'["PlatformHEVCDecoderSupport","VaapiVideoDecoder","AcceleratedVideoDecodeLinuxGL","AcceleratedVideoDecodeLinuxZeroCopyGL"].join(",")'
NEW = b'"PlatformHEVCDecoderSupport,VaapiVideoDecoder,AcceleratedVideoDecodeLinuxGL,AcceleratedVideoDecodeLinuxZeroCopyGL,VaapiOnNvidiaGPUs"'
assert len(OLD) == len(NEW)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("asar", nargs="?", type=Path, default=DEFAULT_ASAR)
    parser.add_argument(
        "--restore", action="store_true", help="Restore the .orig backup."
    )
    args = parser.parse_args()
    asar: Path = args.asar
    backup = asar.with_name(asar.name + ".orig")

    if args.restore:
        shutil.move(backup, asar)
        print(f"restored {asar}")
        return

    data = asar.read_bytes()
    if NEW in data:
        print(f"{DEFAULT_ASAR} already patched.")
        return
    if data.count(OLD) != 1:
        sys.exit("feature list not found. Foxglove version changed?")
    if not backup.exists():
        shutil.copy2(asar, backup)
    asar.write_bytes(data.replace(OLD, NEW))
    print(f"patched {asar} (backup: {backup})")


if __name__ == "__main__":
    main()
