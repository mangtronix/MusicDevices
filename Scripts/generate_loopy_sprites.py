#!/usr/bin/env python3
"""
generate_loopy_sprites.py
Run this on your computer (not on CircuitPython) to create loopy_sprites.bmp.
The BMP is written to ../CircuitPython/loopy_sprites.bmp regardless of where
you run the script from. Copy it to your CIRCUITPY drive when ready.

  python3 Scripts/generate_loopy_sprites.py

No external libraries needed -- uses only the standard library.

Layout:
  16 tiles arranged horizontally. Tile index = bitmask of playing clips.
  Colors match Loopy Pro's default clip palette:
    bit 0 = drums   (orange)
    bit 1 = voice   (yellow)
    bit 2 = guitar  (lime)
    bit 3 = keys    (blue)
  So tile 0 = no clips, tile 15 = all four clips playing.

Each tile draws four vertical "VU" bars, one per clip. A clip that is
playing shows a tall bright bar in its color; a clip that is not playing
shows a short dim base in its color.
"""

import os
import struct

# Output goes alongside loopy_simple.py so it can be picked up by CircuitPython
OUTPUT_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "CircuitPython", "loopy_sprites.bmp",
))

# --- Sprite sheet layout -----------------------------------------------------
TILE   = 32
NTILES = 16
WIDTH  = TILE * NTILES   # 512
HEIGHT = TILE             # 32

# --- Palette (8-bit indexed) -------------------------------------------------
# Indices 0..9; everything else stays black.
BG    = 0
WHITE = 1

# Bright per-clip
B_DRUMS  = 2
B_VOICE  = 3
B_GUITAR = 4
B_KEYS   = 5

# Dim per-clip
D_DRUMS  = 6
D_VOICE  = 7
D_GUITAR = 8
D_KEYS   = 9

# Loopy Pro default clip colors
PALETTE = [(0, 0, 0)] * 256
PALETTE[WHITE]    = (255, 255, 255)
PALETTE[B_DRUMS]  = (255, 110,   0)   # orange
PALETTE[B_VOICE]  = (255, 230,   0)   # yellow
PALETTE[B_GUITAR] = (155, 255,  31)   # lime
PALETTE[B_KEYS]   = ( 30, 130, 255)   # blue
PALETTE[D_DRUMS]  = ( 60,  26,   0)
PALETTE[D_VOICE]  = ( 60,  54,   0)
PALETTE[D_GUITAR] = ( 36,  60,   8)
PALETTE[D_KEYS]   = (  8,  32,  60)

BRIGHT = [B_DRUMS, B_VOICE, B_GUITAR, B_KEYS]
DIM    = [D_DRUMS, D_VOICE, D_GUITAR, D_KEYS]

# --- Drawing helpers ---------------------------------------------------------
def blank():
    return [[BG] * TILE for _ in range(TILE)]

def fill_rect(t, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            if 0 <= x < TILE and 0 <= y < TILE:
                t[y][x] = c

def state_tile(state):
    """state is a 4-bit bitmask: bit i = clip i is playing."""
    t = blank()

    # 4 columns of width 8 across the 32px tile.
    # Each bar uses x=col*8+1 .. col*8+7 (6px wide).
    for col in range(4):
        active = (state >> col) & 1
        x0 = col * 8 + 1
        x1 = col * 8 + 7

        if active:
            # Tall bright bar from y=4 to y=30, with a white tip
            fill_rect(t, x0, 4,  x1, 30, BRIGHT[col])
            fill_rect(t, x0, 4,  x1, 6,  WHITE)
        else:
            # Short dim base at the bottom
            fill_rect(t, x0, 26, x1, 30, DIM[col])

    # 1px floor across all columns to ground the bars visually
    for x in range(0, TILE):
        t[30][x] = DIM[x // 8]

    return t

# --- BMP writer (8-bit indexed, no compression) ------------------------------
def write_bmp(filename, tiles):
    pixels = [[BG] * WIDTH for _ in range(HEIGHT)]
    for ti, tile in enumerate(tiles):
        for y in range(TILE):
            for x in range(TILE):
                pixels[y][ti * TILE + x] = tile[y][x]

    row_size      = WIDTH                    # 512, multiple of 4
    pixel_data_sz = HEIGHT * row_size
    palette_sz    = 256 * 4
    header_sz     = 14 + 40
    offset        = header_sz + palette_sz
    file_size     = offset + pixel_data_sz

    with open(filename, 'wb') as f:
        # BMP file header (14 bytes)
        f.write(b'BM')
        f.write(struct.pack('<I', file_size))
        f.write(struct.pack('<HH', 0, 0))
        f.write(struct.pack('<I', offset))

        # DIB info header (40 bytes)
        f.write(struct.pack('<I', 40))
        f.write(struct.pack('<i', WIDTH))
        f.write(struct.pack('<i', HEIGHT))
        f.write(struct.pack('<HH', 1, 8))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', pixel_data_sz))
        f.write(struct.pack('<ii', 2835, 2835))
        f.write(struct.pack('<I', 256))
        f.write(struct.pack('<I', 0))

        # Palette (BMP stores BGRA)
        for r, g, b in PALETTE:
            f.write(struct.pack('BBBB', b, g, r, 0))

        # Pixel data, bottom-to-top
        for y in range(HEIGHT - 1, -1, -1):
            f.write(bytes(pixels[y]))

    print("Created %s  (%dx%d px, 8-bit indexed BMP)" % (filename, WIDTH, HEIGHT))

# --- Build -------------------------------------------------------------------
tiles = [state_tile(i) for i in range(NTILES)]
write_bmp(OUTPUT_PATH, tiles)
print("Copy %s to your CIRCUITPY drive." % os.path.basename(OUTPUT_PATH))
