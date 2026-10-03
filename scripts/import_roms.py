#!/usr/bin/env python3
"""
ROM Import and Validation Utility for UNO Q Arena.
Scans user directory for legally obtained ROMs and integrates them with Libretro.
"""

import argparse
import hashlib
import os
import shutil
import sys

def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Import ROMs into UNO Q Arena")
    parser.add_argument("--roms-dir", default="roms", help="Directory containing user ROM files")
    parser.add_argument("--integrate", action="store_true", help="Register with stable_retro integration")
    args = parser.parse_args()

    if not os.path.exists(args.roms_dir):
        print(f"Error: Directory '{args.roms_dir}' not found.")
        sys.exit(1)

    print(f"Scanning for ROMs in: {args.roms_dir}")
    valid_exts = {".md", ".bin", ".gen", ".sfc", ".smc", ".nes", ".gba", ".chd", ".iso"}
    found_roms = []

    for root, _, files in os.walk(args.roms_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in valid_exts:
                p = os.path.join(root, f)
                found_roms.append(p)

    print(f"Found {len(found_roms)} ROM candidate(s):")
    for r in found_roms:
        checksum = sha256_file(r)
        print(f"  - {os.path.basename(r)} (SHA256: {checksum[:12]}...)")

    if args.integrate:
        try:
            import stable_retro as retro
            print("\nIntegrating ROMs with stable-retro...")
            retro.data.merge(args.roms_dir)
            print("ROM integration complete!")
        except Exception as e:
            print(f"Integration notice: {e}")


if __name__ == "__main__":
    main()
