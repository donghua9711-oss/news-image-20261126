# The Day in Full — News Image, 26 November 2026

[![Competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/donghua9711-oss/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/donghua9711-oss/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

One page, one day: a 1024×1024 newspaper front page summing up the world
news of **Thursday 26 November 2026** — 30 verified stories from 7 regions,
each credited to the outlet that reported it.

## What is on the page

- A masthead with the day's date and the region tally
- "The Day in UTC" — the day's verified clock moments
- Three illustrated lead stories (US tariffs, the Asian market plunge,
  Ukraine's strike on the Savasleyka air base)
- Eight further drawn stories as numbered row cards
- A dot-matrix world map with numbered pins for the 11 drawn stories
- Nineteen one-line briefs covering the rest of the day
- A date-check footer: every story happened, or was first reported, on
  26 November 2026 in some time zone

## How it is built

- `compose.py` draws the page with PIL from the story data and the three
  illustrations in `assets/`, and writes `entry.png`.
- `SOURCES.md` lists every story with its outlet and report date.
- `main.ts` is the entry program: it copies the committed `entry.png` to
  the output folder and verifies the copy (PNG signature, 1 MiB cap,
  1024×1024 cap, byte-for-byte read-back), so repeated runs always
  deliver the identical file.
