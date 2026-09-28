#!/usr/bin/env python3
"""Derive pixel-rendered Ashen Oath combat sprites from Kenney Particle Pack."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "Docs/AssetArchives/kenney_particle-pack.zip"
OUTPUT = ROOT / "Assets/Resources/VFX"

SPRITES = {
    "telegraph_ring.png": ("circle_01.png", 72),
    "hit_slash.png": ("slash_04.png", 96),
    "dodge_flash.png": ("magic_03.png", 96),
    "reward_glint.png": ("star_06.png", 64),
    "healing_burst.png": ("magic_04.png", 96),
    "craft_flare.png": ("flare_01.png", 96),
    "harvest_glint.png": ("star_07.png", 64),
    "fishing_ripple.png": ("circle_02.png", 96),
}


def derive(source: Image.Image, size: int) -> Image.Image:
    """Pixelate the luminance mask and turn it into a white tintable sprite."""
    mask = source.convert("RGBA").resize((size, size), Image.Resampling.NEAREST)
    output = Image.new("RGBA", mask.size, (255, 255, 255, 0))
    intensities = [
        (alpha * (red + green + blue) // 3) // 255
        for red, green, blue, alpha in mask.getdata()
    ]
    peak = max(intensities) or 1
    output.putdata([
        (255, 255, 255, round((intensity / peak) ** 0.68 * 255))
        for intensity in intensities
    ])
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify generated files match the archive")
    args = parser.parse_args()
    if not ARCHIVE.is_file():
        raise SystemExit(f"Missing licensed source archive: {ARCHIVE}")

    outputs = []
    with zipfile.ZipFile(ARCHIVE) as archive:
        for filename, (source_name, size) in SPRITES.items():
            member = f"PNG (Transparent)/{source_name}"
            with archive.open(member) as source_file:
                with Image.open(source_file) as source:
                    derived = derive(source, size)
            path = OUTPUT / filename
            if args.check:
                if not path.is_file():
                    raise SystemExit(f"Missing generated VFX: {path}")
                with Image.open(path) as actual:
                    if actual.convert("RGBA").tobytes() != derived.tobytes():
                        raise SystemExit(f"Generated VFX is stale: {path}")
            else:
                OUTPUT.mkdir(parents=True, exist_ok=True)
                derived.save(path, optimize=True)
            outputs.append(f"{filename}: {size}x{size}")

    for line in outputs:
        print(line)


if __name__ == "__main__":
    main()
