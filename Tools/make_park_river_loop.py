#!/usr/bin/env python3
"""Build the seamless Unity river ambience from its preserved CC0 source excerpt."""

from __future__ import annotations

from array import array
import hashlib
from pathlib import Path
import struct
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Docs/AssetArchives/park-ambiences-cc0/park_ambience_river_source_excerpt.wav"
OUTPUT = ROOT / "Assets/Resources/Audio/Ambience/park_ambience_river.wav"
SAMPLE_RATE = 48_000
CROSSFADE_SECONDS = 2


def locate_chunks(wave: bytes) -> tuple[int, int, tuple[int, int, int, int, int, int, int]]:
    if wave[:4] != b"RIFF" or wave[8:12] != b"WAVE":
        raise ValueError("Source is not a RIFF/WAVE file")

    offset = 12
    format_data = None
    data_chunk = None
    while offset + 8 <= len(wave):
        chunk_id = wave[offset:offset + 4]
        chunk_size = struct.unpack_from("<I", wave, offset + 4)[0]
        content_offset = offset + 8
        if content_offset + chunk_size > len(wave):
            raise ValueError(f"Truncated WAV chunk {chunk_id!r}")
        if chunk_id == b"fmt ":
            format_data = struct.unpack_from("<HHIIHH", wave, content_offset)
        elif chunk_id == b"data":
            data_chunk = (offset, content_offset, chunk_size)
            break
        offset = content_offset + chunk_size + (chunk_size & 1)

    if format_data is None or data_chunk is None:
        raise ValueError("WAV must contain fmt and data chunks")
    header_offset, data_offset, data_size = data_chunk
    return header_offset, data_offset, (*format_data, data_size)


def main() -> None:
    wave = SOURCE.read_bytes()
    data_header_offset, data_offset, fmt = locate_chunks(wave)
    format_tag, channels, sample_rate, byte_rate, block_align, bit_depth, data_size = fmt
    if (format_tag, channels, sample_rate, block_align, bit_depth) != (1, 2, SAMPLE_RATE, 4, 16):
        raise ValueError(f"Expected 48 kHz stereo 16-bit PCM, got {fmt}")
    data = wave[data_offset:data_offset + data_size]
    data = data[:len(data) - len(data) % block_align]

    pcm = array("h")
    pcm.frombytes(data)
    if pcm.itemsize != 2:
        raise RuntimeError("This script requires 16-bit native array elements")
    if sys.byteorder != "little":
        pcm.byteswap()

    frame_count = len(pcm) // channels
    fade_frames = SAMPLE_RATE * CROSSFADE_SECONDS
    if frame_count <= fade_frames * 4:
        raise ValueError("Source excerpt is too short for a safe crossfade")

    interior = pcm[fade_frames * channels:(frame_count - fade_frames) * channels]
    beginning = pcm[:fade_frames * channels]
    ending = pcm[(frame_count - fade_frames) * channels:]
    crossfade = array("h")
    for frame in range(fade_frames):
        weight = frame / (fade_frames - 1)
        for channel in range(channels):
            index = frame * channels + channel
            sample = round(ending[index] * (1.0 - weight) + beginning[index] * weight)
            crossfade.append(max(-32768, min(32767, sample)))

    output_samples = interior + crossfade
    if sys.byteorder != "little":
        output_samples.byteswap()
    output_data = output_samples.tobytes()
    output_wave = bytearray(wave[:data_offset] + output_data)
    struct.pack_into("<I", output_wave, 4, len(output_wave) - 8)
    struct.pack_into("<I", output_wave, data_header_offset + 4, len(output_data))
    OUTPUT.write_bytes(output_wave)

    duration = len(output_samples) / channels / sample_rate
    digest = hashlib.sha256(output_wave).hexdigest()
    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {len(output_wave):,} bytes, {duration:.3f}s, SHA-256 {digest}")


if __name__ == "__main__":
    main()
