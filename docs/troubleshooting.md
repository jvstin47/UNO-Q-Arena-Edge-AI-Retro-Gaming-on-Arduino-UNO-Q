# Troubleshooting Guide

Common issues and troubleshooting steps when developing and running **UNO Q Arena**.

## 1. No Gamepad or Hardware Controller Detected
- **Issue**: Console logs `[Input] No gamepad found. Defaulting to keyboard controls.`
- **Resolution**: Use keyboard controls (WASD for D-Pad, J/K/L for punches, U/I/O for kicks, Enter for Start). If using USB gamepad, verify it is recognized by OS via `lsusb` or System Settings.

## 2. Audio Crackling or Stutter
- **Issue**: Audio chops or lags behind video.
- **Resolution**: Adjust `buffer_size` in `AudioManager(buffer_size=1024)` or run with `--no-audio` if testing on resource-constrained development hosts.

## 3. Serial Port Permission Denied
- **Issue**: `PermissionError: [Errno 13] Permission denied: '/dev/ttyACM0'`
- **Resolution**: Add user to `dialout` group:
  ```bash
  sudo usermod -a -G dialout $USER
  ```

## 4. Libretro ROM Not Found
- **Issue**: `ROM for 'StreetFighterIISpecialChampionEdition-Genesis-v0' not found. Starting Mock Combat Arena.`
- **Resolution**: The project falls back seamlessly to the built-in zero-ROM Mock Arena. To use official game ROMs, import your Genesis ROM using `python scripts/import_roms.py --roms-dir ./roms --integrate`.
