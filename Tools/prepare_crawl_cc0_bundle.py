#!/usr/bin/env python3
"""Fetch the pinned CC0 Crawl tiles used by Ashen Oath and build a reviewable bundle."""

import hashlib
import struct
import urllib.request
import zipfile
from pathlib import Path

from crawl_creature_data import CREATURES, SOURCE_COMMIT, SOURCE_RELEASE, SOURCE_REPOSITORY

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "Docs/AssetArchives/crawl-cc0-creatures.zip"
LICENSE_DIR = ROOT / "Docs/Licenses/crawl-tiles"
DOCS = ("README.md", "ARTISTS.md", "TILES_UNDER_UNKNOWN_LICENSE.md")


def fetch(path: str) -> bytes:
    url = f"https://raw.githubusercontent.com/crawl/tiles/{SOURCE_COMMIT}/{path}"
    request = urllib.request.Request(url, headers={"User-Agent": "AshenOathAssetAudit/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def main() -> None:
    if len(CREATURES) != 55 or len({row[1] for row in CREATURES}) != 55:
        raise SystemExit("The curated set must contain 55 distinct source files.")

    source_docs = {name: fetch(name).decode("utf-8") for name in DOCS}
    unknown_names = {
        line.removeprefix("- ").strip().casefold()
        for line in source_docs["TILES_UNDER_UNKNOWN_LICENSE.md"].splitlines()
        if line.startswith("- ")
    }
    collisions = [Path(row[1]).name for row in CREATURES
                  if Path(row[1]).name.casefold() in unknown_names]
    if collisions:
        raise SystemExit("Selected files appear in the upstream unclear-license list: " + ", ".join(collisions))

    payloads: dict[str, bytes] = {}
    for _, source_path, *_ in CREATURES:
        archive_path = f"{SOURCE_RELEASE}/{source_path}"
        data = fetch(archive_path)
        if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 24:
            raise SystemExit(f"Source is not a valid PNG: {archive_path}")
        width, height = struct.unpack(">II", data[16:24])
        if (width, height) != (32, 32):
            raise SystemExit(f"Expected a 32x32 tile, got {width}x{height}: {archive_path}")
        payloads[archive_path] = data

    LICENSE_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in source_docs.items():
        (LICENSE_DIR / name).write_text(content, encoding="utf-8")
    notice = (
        "Crawl Stone Soup tile subset used in Ashen Oath\n"
        f"Source repository: {SOURCE_REPOSITORY}\n"
        f"Pinned commit: {SOURCE_COMMIT}\n"
        f"Source release folder: {SOURCE_RELEASE}\n"
        "The upstream README identifies the exported tiles as CC0 (public domain) and links its approved-artists list and separate unclear-license exclusion list. "
        "The 55 selected PNGs are unchanged 32x32 sprites and their source paths are recorded in crawl-creatures-map.tsv. "
        "The upstream README, ARTISTS.md, and TILES_UNDER_UNKNOWN_LICENSE.md are retained alongside this notice.\n"
    )
    (LICENSE_DIR / "NOTICE.txt").write_text(notice, encoding="utf-8")

    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, content in sorted(payloads.items()):
            archive.writestr(path, content)
        for name, content in source_docs.items():
            archive.writestr(f"license/{name}", content.encode("utf-8"))
        archive.writestr("license/NOTICE.txt", notice.encode("utf-8"))

    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    print(f"Bundled {len(payloads)} pinned 32x32 CC0 sprites.")
    print(f"Archive: {ARCHIVE.relative_to(ROOT)} ({ARCHIVE.stat().st_size:,} bytes)")
    print(f"SHA-256: {digest}")
    print(f"License files: {LICENSE_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
