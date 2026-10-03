#!/usr/bin/env python3
"""
Environment and hardware validation script for UNO Q Arena.
"""

import sys
import os

def check():
    print("=" * 60)
    print("  UNO Q Arena Environment Verification")
    print("=" * 60)

    # 1. Python version
    v = sys.version_info
    print(f"Python Version: {v.major}.{v.minor}.{v.micro} -> {'OK' if v.major == 3 and v.minor >= 10 else 'FAIL'}")

    # 2. Package Imports
    packages = [
        ("numpy", "NumPy"),
        ("pygame", "Pygame (Rendering & Audio)"),
        ("yaml", "PyYAML"),
        ("serial", "PySerial (IPC Link)"),
        ("onnxruntime", "ONNX Runtime (Neural Inference)"),
        ("stable_retro", "Stable-Retro / Libretro"),
    ]

    all_passed = True
    for mod, label in packages:
        try:
            __import__(mod)
            print(f"  [+] {label}: Available")
        except ImportError:
            print(f"  [-] {label}: NOT FOUND")
            all_passed = False

    # 3. Model check
    model_path = "models/policies/sample_policy.onnx"
    if os.path.exists(model_path):
        print(f"  [+] Pre-trained Policy Model: Found ({model_path})")
    else:
        print(f"  [-] Pre-trained Policy Model: Missing ({model_path})")

    # 4. Hardware Port Check
    ports = ["/dev/ttyACM0", "/dev/ttyUSB0", "/dev/cu.usbmodem1101", "/dev/rpmsg0"]
    found_port = any(os.path.exists(p) for p in ports)
    if found_port:
        print("  [+] Hardware Coprocessor: Detected port")
    else:
        print("  [*] Hardware Coprocessor: Not connected (Mock IPC available)")

    print("=" * 60)
    if all_passed:
        print(" Environment check PASSED! Ready to run UNO Q Arena.")
    else:
        print(" Environment check FAILED. Please run: pip install -e .")
    print("=" * 60)


if __name__ == "__main__":
    check()
