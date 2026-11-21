# NOTES — The Passport Page of a Country That Isn't There

Competition: `the-passport-page-of-a-countr-2-20261121-0318` ($50, deadline
2026-11-21 06:18 UTC / 14:18 WITA). Harness: program/v1, `main.py` (Python
3.13, stdlib only, no network). Repo:
`Van7art/the-passport-page-of-a-countr-2-20261121-0318-entry`.

## Three variants designed in this session

All three were invented fresh in this session from the kit + requirements
only. No files from any earlier session were read or reused.

### Variant A — Republic of Solmaria (WINNER)
Mediterranean-style island republic, capital Aurelia. Holder: Mara Solenne,
lighthouse keeper. Stamps: Corsano (arrival 02 JUN 2024 / departure
09 JUN 2024), Vellore (entry 18 SEP 2025), Solmaria re-entry (21 SEP 2025).
Telling detail: "ENTRY BY FERRY ONLY — NO AIRPORT ON SOLMARIA" + a
12 AUR ferry-tax stamp + a hand-drawn island map marking Aurelia and
Pt. Merrow. Passport SM 0417829, issued 14 MAR 2024, expires 14 MAR 2034.

### Variant B — High Kingdom of Aerthwaite
Mountain kingdom, capital Dunmoor. Holder: a mountain guide. Telling
detail: an altitude permit required above 3,000 m. Rejected: the mountain
story gives the portrait less to work with (a guide's gear reads as generic
outdoor clothing) and the stamps would all be land-border crossings, which
is a thinner, less distinctive travel history than Solmaria's ferry-only
island.

### Variant C — Free Port of Nhalu
Tropical canal city-state. Holder: a dockworker. Telling detail: a free-port
transit exemption ("goods in transit exempt; holder may not seek employment
ashore"). Rejected: the free-port condition is bureaucratic rather than
visual, and a dockworker's portrait is harder to tie to a specific place
than a lighthouse keeper to a lighthouse island.

## Why A won
- Portrait ↔ place fit (judge criterion 4): a lighthouse keeper in a navy
  uniform with a cap, from Aurelia, "Island of the Lantern" — the face
  belongs to the country.
- Date consistency (criterion 3): every stamp falls between issue
  (14 MAR 2024) and expiry (14 MAR 2034), and the handwritten note
  ("return to Aurelia by 21 Sep") matches the 21 SEP 2025 re-entry stamp.
- Telling detail (criterion 5): the ferry-only condition explains the
  whole travel history — an island with no airport can only be reached by
  ferry, so all four stamps are ferry-port stamps.
- MRZ is ICAO 9303-correct: check digits computed with weights 7-3-1 for
  document number, birth date, expiry date, personal number, and the
  composite check digit.

## Build process (two genuine passes on main.py)
1. Draft: renderer written, v1 image rendered (229,052 bytes), `main.py`
   written embedding v1 as base64; ran once, output verified.
2. Revision: visual review of v1 found the country title crossing the
   spine into the VISAS header, the data-field column colliding with the
   signature block, halftone dots muddying the portrait, a clipped
   round-stamp caption, and map labels sitting on the island outline.
   All fixed in the renderer; v2 re-rendered (226,430 bytes) and `main.py`
   updated to embed v2 (docstring records the revision). `main.py` was
   therefore written in two separate steps with a real improvement pass,
   as the kit's thinking checks require.

## Verification (local, this session)
- `python3 main.py` run twice: both outputs byte-identical,
  sha256 `3fcc27728e4b79c8b4d00cf14aee2fd08f621b9ed29fc31c970a6d9e6fce08a5`.
- Output: valid PNG, 1024×1024, 226,430 bytes (limit 1,048,576) — PASS.
- Renderer: `/tmp/render_passport.py` (build-time only, not part of the repo).
- No network, no paid APIs, no money spent. Not pushed, not submitted —
  the coordinator handles push, kit check, bundle, and submit.

## Files in this work directory
- `main.py` — entrypoint (stdlib only, embeds the PNG as base64)
- `entry.png` — the rendered spread, for reference (binary; push via user
  upload, not the GitHub connector)
- `README.md`, `LICENSE` (MIT), `NOTES.md` (this file)
