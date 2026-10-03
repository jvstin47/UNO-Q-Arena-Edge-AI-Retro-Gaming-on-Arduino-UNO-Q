# Game Manifests (`games/`)

This directory contains metadata, RAM memory addresses, controller button layouts, and ROM validation checksums for supported games.

## Legal Notice Regarding Game ROMs

**No copyrighted ROMs, disc images, or BIOS files are stored in this repository.**

Users must legally source their own game cartridges and dump the ROM files into the `roms/` directory.

To automatically validate and import your ROMs into the Libretro environment:

```bash
python scripts/import_roms.py --roms-dir ./roms
```

## Adding a New Game

To add support for a new game:
1. Create a new YAML manifest under `games/manifests/<game_id>.yaml`.
2. Define the platform, SHA256 checksum, player inputs, and RAM offsets.
3. Test using `uno-q-arena --game <game_id>`.
