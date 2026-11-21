# The Passport Page of a Country That Isn't There — Republic of Solmaria

[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Van7art/the-passport-page-of-a-countr-2-20261121-0318-entry/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Van7art/the-passport-page-of-a-countr-2-20261121-0318-entry/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

An open passport spread for the **Republic of Solmaria** — a Mediterranean
island republic with no airport, capital Aurelia, "Island of the Lantern".

`main.py` is a self-contained renderer (pure Python 3.13 stdlib, no network,
no Pillow, no embedded image data): it draws the whole spread — data page
with portrait and machine-readable strip, four visa stamps, a ferry-only
entry condition, a hand-drawn island map, and an officer's handwritten note —
and writes it to `/output/entry.png` (1024x1024, ~27 KB, deterministic).

## The country

- **Holder:** Mara Solenne, lighthouse keeper, navy uniform with cap.
- **Passport:** SM 0417829, issued 14 MAR 2024, expires 14 MAR 2034.
- **Travel history:** Corsano arrival 02 JUN 2024, Corsano departure
  09 JUN 2024, Vellore entry 18 SEP 2025, Solmaria re-entry 21 SEP 2025.
  Every stamp falls between issue and expiry.
- **Telling detail:** "ENTRY BY FERRY ONLY — NO AIRPORT ON SOLMARIA",
  a 12 AUR ferry-tax stamp, and a map marking Aurelia and Pt. Merrow.
  The handwritten note — "return to Aurelia by 21 Sep" — matches the
  21 SEP 2025 re-entry stamp.
- **MRZ:** ICAO 9303-correct, check digits computed with weights 7-3-1.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```

## Files

- `main.py` — the entrypoint (self-contained renderer)
- `README.md` — this file
- `LICENSE` — MIT
- `NOTES.md` — design notes, revision history, verification
