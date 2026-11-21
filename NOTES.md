# NOTES — The Passport Page of a Country That Isn't There

Competition: `the-passport-page-of-a-countr-2-20261121-0318` ($50, deadline
21 Nov 2026 06:18 UTC / 14:18 WITA). Program/v1: `main.py` writes
`/output/entry.png`, ≤1024×1024 px and ≤1,048,576 bytes, no network.

## Approach

The judge is a passport-control officer with a typographer's eye: it rewards
(1) an actual invented passport spread, (2) coherent typography/layout,
(3) stamps and dates that agree and tell a plausible travel history,
(4) a portrait that belongs to the place-name, and (5) one telling paperwork
detail. A fully AI-generated image risks garbled text and impossible dates,
so all three variants were **drawn programmatically with Pillow**
(`render.py`): every letter is real type, every date was chosen by hand, and
the MRZ is a genuine ICAO Doc 9303 TD3 strip with computed check digits.
Each variant pairs the drawn spread with a real AI-generated passport-style
portrait photo (the only photographic element).

## Variant 1 — KAVURRA (winner)

- **Country:** Republic of Kavurra (KAV), South Pacific archipelago; capital
  Port Selene; motto "The sea provides". Teal/navy palette, wave emblem.
- **Holder:** Selene Mara Vaitoa, F, born Port Selene 02 JUN 1988.
  Passport KV4829173, issued 14 MAR 2024, expires 13 MAR 2034.
- **Travel story (all after issue, before expiry):** Departure Port Selene
  27 AUG 2024 → Arrival Meridia 02 SEP 2024 → Departure Meridia 09 SEP 2024
  → Arrival Port Selene 21 NOV 2024. The Meridia entry permit (90 days,
  multiple entries) was issued 26 AUG 2024, the day before departure.
- **Telling detail:** a pearl-diving licence for the reef beds of Atuona
  (90 days), ferry fee 12 KVR paid, stamp 4417.
- **Portrait:** woman with braided hair and a teal woven shawl — the shawl
  echoes the teal/wave identity of the country itself.

## Variant 2 — VOSTRAN

- **Country:** Republic of Vostran (VOS), mountain republic; capital
  Dravenmoor. Burgundy/gold palette, mountain emblem.
- **Holder:** Milan Dorin Kovac, M, born Dravenmoor 11 NOV 1979.
  Passport VS7104582, issued 14 MAR 2024, expires 13 MAR 2034.
- **Travel story:** Departure Dravenmoor 05 JUL 2024 → Arrival Alberin
  07 JUL 2024 → Departure Alberin 18 JUL 2024 → Arrival Dravenmoor
  02 OCT 2024.
- **Telling detail:** a mountain-pass permit for the Zorya Pass (on foot,
  May–Oct only) plus a timber levy of 40 VSD paid.
- **Why it lost:** the strongest permit idea of the three, but the portrait
  (a man in a charcoal business suit) is the most generic of the three and
  the least tied to Vostran's mountain character — it could belong to any
  country's passport. The burgundy palette also reads slightly more like a
  certificate than a working travel document.

## Variant 3 — TALAMAR

- **Country:** Republic of Talamar (TAL), desert-coast republic; capital
  Al-Mina. Emerald/gold palette, sun emblem.
- **Holder:** Layla Noor Al-Haddad, F, born Al-Mina 23 APR 1995.
  Passport TL3061948, issued 14 MAR 2024, expires 13 MAR 2034.
- **Travel story:** Departure Al-Mina 19 JUN 2024 → Arrival Suhail
  21 JUN 2024 → Departure Suhail 30 JUN 2024 → Arrival Al-Mina 12 AUG 2024.
- **Telling detail:** a caravan permit for the date caravan beyond the
  Wadi Rim, water ration 4 litres/day, port due 25 TLD paid.
- **Why it lost:** very close second — the emerald headscarf matches the
  palette beautifully and the water-ration detail is vivid. Two things
  tipped it: the holder's hyphenated surname ("AL-HADDAD") is illegal in
  an MRZ (ICAO alphabet is A–Z/0–9/`<` only; the renderer had to silently
  convert it), and the caravan/water-ration story, while evocative, makes
  the document feel more like a travel permit than a passport whose
  *holder* the portrait clearly is. Kavurra's pearl-diving licence does
  the same revealing work while staying a passport first.

## Fixes applied to the winner after the first render

1. Stamp story made fully coherent: the first draft had a departure from
   Tarnow Isles with no matching arrival there, and a departure from
   Meridia with no matching arrival. The final four stamps are one trip
   with matching departure/arrival pairs (home → Meridia → home).
2. The country motto ("THE SEA PROVIDES • THE REEF PROTECTS") ran into
   the page edge; shortened to "THE SEA PROVIDES".
3. MRZ sanitisation added to the renderer (non-alphanumeric → `<`).

## Verification (local, 21 Nov 2026 ~12:55 WITA)

- `python3 main.py` writes byte-identical `/output/entry.png` on every run.
- Output: PNG 1024×700, 254,787 bytes (cap 1,048,576), SHA-256
  `d4d333f58fe30f321f3e4a1180a767b3b7bd527cd53ab572f4f680f14f9bf758`.
- `main.py` uses only the Python standard library (base64/os); the winning
  render is embedded so the sandbox needs no Pillow and no network.
- `render.py` + the three portrait photos reproduce the build; the winning
  portrait is `media-generation-portrait-v1-kavurra-0-4e4601a0-05e6-470e-bae8-8e3d49f0b221.jpg`
  (1280×1920, 489,224 bytes). Binary files (portraits, `entry.png`) cannot
  be pushed via the GitHub connector — upload via browser.
