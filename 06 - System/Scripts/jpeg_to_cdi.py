"""
Converts a JPEG image to a raw CD image (.cdr) file.
CDR is a raw ISO 9660 disc image — the native format used by macOS Disk Utility
and compatible with most disc imaging tools (Disk Utility, hdiutil, IsoBuster, etc.).
"""
import io
import os
import pycdlib

JPEG_PATH = r"C:\Users\Arin\OneDrive\Documents\Obsidian Vault\WhatsApp Image 2026-06-27 at 1.24.57 PM.jpeg"
CDR_PATH  = r"C:\Users\Arin\OneDrive\Documents\Obsidian Vault\WhatsApp Image 2026-06-27 at 1.24.57 PM.cdr"


def main():
    print("Building ISO 9660 image from JPEG...")

    iso = pycdlib.PyCdlib()
    iso.new()

    with open(JPEG_PATH, "rb") as fh:
        data = fh.read()

    base = os.path.basename(JPEG_PATH).upper()
    name, ext = (base.rsplit(".", 1) + [""])[:2]
    iso_name = f"/{name[:8]}.{ext[:3]};1" if ext else f"/{name[:8]};1"

    iso.add_fp(io.BytesIO(data), len(data), iso_name)

    with open(CDR_PATH, "wb") as out:
        iso.write_fp(out)

    iso.close()

    size = os.path.getsize(CDR_PATH)
    print(f"Done. CDR file saved: {CDR_PATH}")
    print(f"Size: {size:,} bytes")


if __name__ == "__main__":
    main()
