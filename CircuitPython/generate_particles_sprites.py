#!/usr/bin/env python3
"""
generate_particles_sprites.py
Run this on your computer (not on CircuitPython) to create particles_sprites.bmp.
Then copy particles_sprites.bmp to your CIRCUITPY drive.

  python3 generate_particles_sprites.py

No external libraries needed — uses only the standard library.
"""

import struct
import math

# ─── Sprite sheet layout ──────────────────────────────────────────────────────
# 5 tiles arranged horizontally, matching the spritesheet.gif convention.
# Tile 0: idle (floating stars)
# Tiles 1-4: explosion for each NeoKey button (colors match web example 04)

TILE   = 32        # tile width and height in pixels
NTILES = 5
WIDTH  = TILE * NTILES   # 160
HEIGHT = TILE             # 32

# ─── 8-bit indexed colour palette ────────────────────────────────────────────
# We use indices 0-15; everything else stays black (index 0).
BG    = 0    # black
WHITE = 1    # (255, 255, 255)
LGRAY = 2    # (120, 120, 120)  — dim star
DGRAY = 3    # (50,  50,  50)   — very dim centre cross

# Note 64 (E4) — pink/magenta  hue ≈ 320°
P1 = 4    # (255,  51, 189)  bright
P2 = 5    # (160,  20, 110)  medium
P3 = 6    # ( 70,   5,  45)  dark

# Note 67 (G4) — yellow         hue ≈ 50°
Y1 = 7    # (255, 221,  51)  bright
Y2 = 8    # (160, 130,  15)  medium
Y3 = 9    # ( 75,  60,   3)  dark

# Note 69 (A4) — green          hue ≈ 110°
G1 = 10   # ( 85, 255,  51)  bright
G2 = 11   # ( 35, 155,  15)  medium
G3 = 12   # ( 10,  70,   3)  dark

# Note 71 (B4) — cyan/teal      hue ≈ 170°
C1 = 13   # ( 51, 255, 221)  bright
C2 = 14   # ( 12, 155, 130)  medium
C3 = 15   # (  3,  65,  55)  dark

PALETTE = [(0, 0, 0)] * 256
PALETTE[WHITE] = (255, 255, 255)
PALETTE[LGRAY] = (120, 120, 120)
PALETTE[DGRAY] = (50,  50,  50)
PALETTE[P1]    = (255,  51, 189)
PALETTE[P2]    = (160,  20, 110)
PALETTE[P3]    = (70,    5,  45)
PALETTE[Y1]    = (255, 221,  51)
PALETTE[Y2]    = (160, 130,  15)
PALETTE[Y3]    = (75,   60,   3)
PALETTE[G1]    = (85,  255,  51)
PALETTE[G2]    = (35,  155,  15)
PALETTE[G3]    = (10,   70,   3)
PALETTE[C1]    = (51,  255, 221)
PALETTE[C2]    = (12,  155, 130)
PALETTE[C3]    = (3,    65,  55)

# ─── Drawing helpers ──────────────────────────────────────────────────────────
def blank():
    return [[BG] * TILE for _ in range(TILE)]

def px(tile, x, y, c):
    if 0 <= x < TILE and 0 <= y < TILE:
        tile[y][x] = c

# ─── Tile 0: idle ─────────────────────────────────────────────────────────────
def idle_tile():
    t = blank()
    # Scattered stars at fixed positions (not random so the BMP is reproducible)
    stars = [
        (2, 2, WHITE), (7, 11, LGRAY), (14, 5, WHITE), (20, 2, LGRAY),
        (27, 7, WHITE), (4, 20, LGRAY), (11, 27, WHITE), (18, 22, LGRAY),
        (25, 28, WHITE), (29, 15, LGRAY), (1, 30, LGRAY), (23, 13, WHITE),
        (9, 16, LGRAY), (30, 25, WHITE),
    ]
    for sx, sy, col in stars:
        px(t, sx, sy, col)

    # Centre cross — hints at something about to happen
    cx, cy = 15, 15
    for d in (-2, -1, 0, 1, 2):
        px(t, cx + d, cy, DGRAY)
        px(t, cx, cy + d, DGRAY)
    px(t, cx, cy, WHITE)
    return t

# ─── Tiles 1-4: explosion ─────────────────────────────────────────────────────
def explosion_tile(c1, c2, c3):
    """
    Concentric filled rings fading outward, plus 4 cardinal rays and
    4 diagonal sparkles. Looks like a shockwave blast.
    """
    t = blank()
    cx, cy = 15, 15

    for y in range(TILE):
        for x in range(TILE):
            dx, dy = x - cx, y - cy
            r = math.sqrt(dx * dx + dy * dy)
            if r <= 2:
                t[y][x] = WHITE
            elif r <= 6:
                t[y][x] = c1
            elif r <= 10:
                t[y][x] = c2
            elif r <= 13:
                t[y][x] = c3

    # Cardinal rays: single-pixel lines from ring edge to tile edge
    for i in range(14, 16):
        px(t, cx + i, cy,     c1)
        px(t, cx - i, cy,     c1)
        px(t, cx,     cy + i, c1)
        px(t, cx,     cy - i, c1)

    # Diagonal sparkles
    for i in range(10, 14):
        d = int(i / math.sqrt(2))
        px(t, cx + d, cy - d, c2)
        px(t, cx - d, cy - d, c2)
        px(t, cx + d, cy + d, c2)
        px(t, cx - d, cy + d, c2)

    return t

# ─── BMP writer (8-bit indexed, no compression) ───────────────────────────────
def write_bmp(filename, tiles):
    # Compose all tiles into one wide pixel array
    pixels = [[BG] * WIDTH for _ in range(HEIGHT)]
    for ti, tile in enumerate(tiles):
        for y in range(TILE):
            for x in range(TILE):
                pixels[y][ti * TILE + x] = tile[y][x]

    row_size       = WIDTH          # 160, already a multiple of 4
    pixel_data_sz  = HEIGHT * row_size
    palette_sz     = 256 * 4
    header_sz      = 14 + 40
    offset         = header_sz + palette_sz
    file_size      = offset + pixel_data_sz

    with open(filename, 'wb') as f:
        # ── BMP file header (14 bytes) ──
        f.write(b'BM')
        f.write(struct.pack('<I', file_size))
        f.write(struct.pack('<HH', 0, 0))       # reserved
        f.write(struct.pack('<I', offset))

        # ── DIB info header (40 bytes) ──
        f.write(struct.pack('<I', 40))           # header size
        f.write(struct.pack('<i', WIDTH))
        f.write(struct.pack('<i', HEIGHT))
        f.write(struct.pack('<HH', 1, 8))        # planes=1, bits-per-pixel=8
        f.write(struct.pack('<I', 0))            # no compression (BI_RGB)
        f.write(struct.pack('<I', pixel_data_sz))
        f.write(struct.pack('<ii', 2835, 2835))  # ~72 DPI
        f.write(struct.pack('<I', 256))          # colours in palette
        f.write(struct.pack('<I', 0))            # important colours

        # ── Colour palette (BGRA order in BMP) ──
        for r, g, b in PALETTE:
            f.write(struct.pack('BBBB', b, g, r, 0))

        # ── Pixel data (BMP rows are stored bottom-to-top) ──
        for y in range(HEIGHT - 1, -1, -1):
            f.write(bytes(pixels[y]))

    print(f"Created {filename}  ({WIDTH}×{HEIGHT} px, 8-bit indexed BMP)")

# ─── Build and write ──────────────────────────────────────────────────────────
tiles = [
    idle_tile(),
    explosion_tile(P1, P2, P3),   # tile 1 — note 64 (E4) pink
    explosion_tile(Y1, Y2, Y3),   # tile 2 — note 67 (G4) yellow
    explosion_tile(G1, G2, G3),   # tile 3 — note 69 (A4) green
    explosion_tile(C1, C2, C3),   # tile 4 — note 71 (B4) cyan
]

write_bmp('particles_sprites.bmp', tiles)
print("Copy particles_sprites.bmp to your CIRCUITPY drive.")
