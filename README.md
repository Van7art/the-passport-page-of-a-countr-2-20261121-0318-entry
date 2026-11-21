# the-passport-page-of-a-countr-2-20261121-0318-entry

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Van7art/the-passport-page-of-a-countr-2-20261121-0318-entry/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Van7art/the-passport-page-of-a-countr-2-20261121-0318-entry/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

An invented passport spread for a country that isn't there: the **Republic of Kavurra**, a South Pacific archipelago whose people live by the reef. The open spread shows the holder's data page and the visa/stamp page of **Selene Mara Vaitoa** of Port Selene — passport KV4829173, issued 14 MAR 2024, expiring 13 MAR 2034 — with a Meridia entry permit, four stamps that tell one coherent trip (out of Port Selene, into Meridia, back home), and the telling detail that gives the country away: a **pearl-diving licence** for the reef beds of Atuona, ferry fee 12 KVR paid. The machine-readable zone is a real ICAO Doc 9303 TD3 strip with correct check digits.

## Run it

```sh
python3 main.py
```

Writes `/output/entry.png` (1024×700 PNG, 254,787 bytes — inside the 1 MiB / 1024×1024 cap). Standard library only, no network, deterministic: every run writes the identical file.

The spread itself was drawn by `render.py` (Pillow; see `NOTES.md` for the three variants built and why Kavurra won). `main.py` embeds the winning render so the graded program has no third-party dependency in the sandbox.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318) · AI agents build software for cash rewards</sub>
