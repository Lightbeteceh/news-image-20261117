# The World in One Day — 17 November 2026

Entry for the [make.fun bounty `news-image-20261117`](https://make.fun/bounty/news-image-20261117):
**"Sum up 17 November's world news in one image."**

![Front page, Tuesday 17 November 2026](entry.png)

## What it is

A newspaper front page — **"THE WORLD IN ONE DAY"** — summing up Tuesday
17 November 2026 in **36 stories across 6 continents**, rendered
programmatically (Python + PIL, DejaVu fonts) so every headline is crisp and
legible. No AI image generation was used for the page itself: image
generators garble long text, and this page is meant to be read.

**Design (v3 — Vintage, chosen by Zis):** classic 19th-century broadsheet —
warm cream paper, black ink, serif throughout (DejaVu Serif), centred
ornate masthead, drop-cap lead paragraph, thin double rules, and a dark-red
accent used sparingly (the word **FALLS**). Same 36 stories as v2.1; only
the presentation changed. Earlier designs are preserved in the project
notes (v1 newspaper, v2/v2.1 SaaS hero).

`render.py` renders `entry.png` from the story data in `stories.py`
(Python 3, Pillow, DejaVu fonts, all local, deterministic).

## Lead stories

1. **KERCH BRIDGE FALLS** — Ukraine struck the 19 km bridge to Crimea for a
   second straight night; a road span collapsed into the strait. Russia hit
   two Kyiv bridges, killing at least two.
2. **IRAN DRONES AT US RADAR IN BAHRAIN** — third attack in five days on the
   Gulf island, home of the US 5th Fleet. Bahrain says it intercepted the
   drones; no casualties reported.
3. **TRUMP, XI & PUTIN TO MEET IN SHENZHEN** — China confirms a trilateral
   summit on Thursday 19 Nov on the APEC sidelines.
4. **TANKERS HIT BY MINES NEAR HORMUZ** — a fourth tanker catches fire in
   24 hours; a third US carrier, USS Theodore Roosevelt, arrives.

Plus 32 more: the EU's Rwanda return-hub plan, Japan scrambling jets over
suspected Russian aircraft, the Pentagon's 9th failed audit, US measles at
its highest since 1991, DR Congo's Ebola outbreak, Pope Leo XIV's Peru
farewell, and more — grouped by region, with a schematic world map marking
where each lead story happened.

## How it runs

```sh
python3 main.py   # writes /output/entry.png
```

`main.py` copies the bundled `entry.png` to `/output/entry.png` — no
network, no timestamps, no randomness. Running it twice produces
byte-identical output. The image was produced by `render.py` in this repo
(Python 3, Pillow, DejaVu fonts, all local).

## Verification

- Image: 1024×1024 px PNG, ~155 KB (limit: 1 MiB, 1024×1024)
- Two runs of `main.py` → identical SHA-256
- Read at full size: all 36 headlines legible, no overflow or clipping

## Sources

Headlines were researched from reporting published 17 November 2026,
including AP, Reuters, AFP, BBC, The Guardian, Al Jazeera, Just Security,
and national outlets. Disputed figures are attributed on the page and in
the research notes (e.g. Moscow's claimed drone-intercept total; the
India bus-crash toll, reported as 6–8 because sources differed). See
`EVIDENCE.md` for the story list and sources.

## License

MIT — see `LICENSE`.
