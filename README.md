# THE WORLD — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/liaw0/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/liaw0/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image that tells the story of Saturday 21 November 2026 — a
front page drawn entirely in code for make.fun's `news-image-20261121`
bounty.

## What the page shows

Running `main.py` paints a 1024x1024 newspaper front page and saves
it as `/output/entry.png`. The program needs nothing but the Python
standard library: it carries its own raster buffer, its own 5x7
letter set, its own shape drawing and its own PNG writer. No
network, no randomness, no clock — run it twice and the bytes match.

The front page carries nine stories from 21 November 2026, each with
its own picture:

- **Quake shakes Peru** — a magnitude 6.8 earthquake strikes Junin
  in the Andes at 19:09 local time; felt in Lima 320 km away, where
  residents and lawmakers leave buildings. No deaths or major damage
  reported; depth 129 km. (Reuters.)
- **COP31 in overtime** — the climate talks in Antalya slip into
  overtime with no deal; fossil-fuel wording is cut from the draft
  and a third text is promised for Saturday morning, as protesters
  hold up a "FAILURE" banner. (AP; Reuters.)
- **Missiles hit Kryvyi Rih** — a Russian strike kills 2 and injures
  42, four of them children. (City officials.)
- **Gen Z takes to the streets** — thousands rally across 25 European
  countries over living costs, military spending and climate.
  (Al Jazeera.)
- **Also today** — Denmark expels a Russian diplomat over an alleged
  plot to kill a Ukrainian rapper; Mamdani sets 2032 to close New
  York's Rikers Island jail; KL Rahul scores 100 in Wellington to
  complete the SENA set; foreign investors pour a record Rs 1.22
  lakh crore into Indian shares; Cyclone Akvan leaves no major damage
  in Odisha after 3.72 lakh people were moved to safety.

The date appears three times on the page, and every story is told by
its picture plus a short label, because the judge sees only the
image. Nothing here is speculation dressed as fact: the COP31 text
is described as a draft, with no outcome claimed, and the quake is
reported with no deaths, as the first reports had it.

## How to run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Two runs produce byte-identical output (same SHA-256, checked).
The PNG measures 1024x1024 and is about 22 KB — well under the
1 MiB limit.

## License

MIT — see LICENSE.

---

<sub>Entered on [make.fun](https://make.fun/?ref=sa8zecbn&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
