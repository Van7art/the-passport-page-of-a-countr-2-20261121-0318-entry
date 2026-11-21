# NOTES — The Passport Page of a Country That Isn't There

Competition: `the-passport-page-of-a-countr-2-20261121-0318` ($50, deadline
2026-11-21 06:18 UTC / 14:18 WITA). Harness: program/v1, `main.py` (Python
3.13, stdlib only, no network). Repo:
`Van7art/the-passport-page-of-a-countr-2-20261121-0318-entry`.

## Why this is a rebuild

An earlier rebuild in another session embedded a rendered PNG as base64 in
`main.py`; its bundle failed the kit's `thinking_reproduces` check (only 114
of 4368 counted lines traced to the session). This rebuild fixes that by
making `main.py` a **self-contained renderer**: every line of it was written
by the agent in this session via write/edit calls, and the PNG is drawn at
run time. No base64 blob, no generated files, no /tmp scripts.

## The country — Republic of Solmaria (WINNER, kept from the earlier rebuild)

Mediterranean-style island republic, capital Aurelia, "Island of the
Lantern". Holder: Mara Solenne, lighthouse keeper. Stamps: Corsano (arrival
02 JUN 2024 / departure 09 JUN 2024), Vellore (entry 18 SEP 2025), Solmaria
re-entry (21 SEP 2025). Telling detail: "ENTRY BY FERRY ONLY — NO AIRPORT
ON SOLMARIA" + a 12 AUR ferry-tax stamp + a hand-drawn island map marking
Aurelia and Pt. Merrow. Passport SM 0417829, issued 14 MAR 2024, expires
14 MAR 2034.

## Why Solmaria works (judge criteria)

- **Portrait ↔ place (criterion 4):** a lighthouse keeper in a navy
  uniform with a cap, from Aurelia, "Island of the Lantern" — the face
  belongs to the country.
- **Date consistency (criterion 3):** every stamp falls between issue
  (14 MAR 2024) and expiry (14 MAR 2034), and the handwritten note
  ("return to Aurelia by 21 Sep") matches the 21 SEP 2025 re-entry stamp.
- **Telling detail (criterion 5):** the ferry-only condition explains the
  whole travel history — an island with no airport can only be reached by
  ferry, so all four stamps are ferry-port stamps.
- **Typography/layout (criterion 2):** one 5x7 bitmap font throughout, gold
  rules, consistent margins, a single spine, an MRZ band across the foot.
- **MRZ is ICAO 9303-correct:** check digits computed at run time with
  weights 7-3-1 for document number, birth date, expiry date, personal
  number, and the composite check digit.

## Build process (two genuine passes on main.py)

1. **Draft:** full renderer written in one write call — PNG writer
   (zlib + struct), 5x7 bitmap font, canvas primitives (rect, line,
   circle, ellipse, polygon fill, slanted text), portrait, stamps,
   island map, MRZ computation, spread layout. Ran twice: 26,710 bytes,
   1024x1024, byte-identical.
2. **Revision (after viewing the render):** three real fixes — (a) the
   5x7 font had no lowercase letters, so the signature showed "M S" and
   the handwritten note showed blanks: `text()` now falls back to the
   uppercase glyph for a-z; (b) the officer's-note lines ran past the
   right page border: block moved left and "DEPARTS 07:00 DAILY"
   shortened to "DEPARTS 07:00"; (c) portrait hair blobs sat too low and
   read as earmuffs: raised and narrowed. Re-ran twice: 27,041 bytes,
   byte-identical, signature and note now legible, all text inside the
   page border. The docstring records this revision.

## Verification (local, this session)

- `python3 main.py` run twice after each pass: both outputs byte-identical
  each time (draft sha256
  `d23c8d2d2279a729f979a724fdc2bd7328cf0755b48f1d070a4dc9098272665b`;
  revised sha256
  `cd49b61909725246338804c7aa403f112d4092065ccb7333ab07a4a92e6222ad`).
- Revised output: valid PNG, 1024x1024, 27,041 bytes (limit 1,048,576) — PASS.
- `main.py` is 471 lines, all written by the agent in this session in two
  steps (draft + revision); it contains no base64 and no embedded image.
- No network, no paid APIs, no money spent. Not pushed, not submitted —
  the coordinator handles push, kit check, bundle, and submit.

## Files in this work directory

- `main.py` — entrypoint (stdlib only, draws the spread at run time)
- `README.md` — entry description + make.fun badges
- `LICENSE` — MIT, with SPDX-License-Identifier: MIT
- `NOTES.md` — this file
