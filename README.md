# The World in One Image — Wednesday 25 November 2026

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/nemesisbug/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)
[![reward](https://make.fun/badge/news-image-20261125/nemesisbug/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

A front page summing up the world's news of Wednesday 25 November 2026 in
one image: China's Shenzhou-24 lifts off with the first Pakistani ever in
space, the US Army prepares to detonate 9,500 lb of unstable explosive in
Iowa, Washington is poised to unveil new tariffs on 16 trading partners,
Berlin forecasts tax revenue past €1 trillion, America hits the road for
Thanksgiving, and the UN marks the day to end violence against women.

## How it is made

`build_image.py` draws the 1024×1024 front page from scratch with Pillow
(masthead, lead art panel, three story cards, Thanksgiving band, briefs,
numbers strip, footer) and writes `entry.png`. `main.py` is the graded
entrypoint: it copies the shipped `entry.png` to the output directory, so
both graded runs write identical bytes.

```sh
python3 build_image.py        # renders entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Stories on the page (all first reported, or happening, on 25 Nov 2026)

1. **Shenzhou-24 launches** — Long March-2F lifts off from Jiuquan at
   00:18 UTC with Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali; Ali is the
   first Pakistani in orbit and the first foreign astronaut to visit
   Tiangong. Docking later today; he will spend 5–10 days aboard running
   four joint China–Pakistan experiments. Sources: Reuters, Xinhua,
   Wikipedia.
2. **Iowa lead-azide detonation** — the US Army will detonate 9,500 lb
   (68 drums) of degraded lead azide at the Iowa Army Ammunition Plant,
   Middletown, at 9 a.m. today; nearby residents were told to leave or
   stay indoors, and a lead-dust plume may drift 100 miles. Sources: AP,
   Wikipedia.
3. **New US tariffs due today** — the Trump administration is poised to
   unveil duties on 16 trading partners after a Section 301 probe into
   excess factory capacity; findings expected as soon as today. Sources:
   Reuters via BusinessWorld (25 Nov).
4. **Germany's tax tops €1 trillion** — Berlin forecasts record tax
   revenue of more than one trillion euros in 2027. Source: The Germany
   Eye (25 Nov).
5. **Thanksgiving eve travel** — Wednesday is the peak outbound day:
   AAA forecasts 81.5 million Americans travelling; TSA expects about
   17.6 million screenings 24–30 Nov; the FAA calls it the busiest
   skies in 16 years. Sources: AAA, TSA, FAA.
6. **International Day for the Elimination of Violence against Women**
   — the UN observance falls today, 25 November.
7. **Spain votes Sunday** — polls put the conservative People's Party
   ahead of the Socialists in the 29 November general election.
8. **Robot rides to the ISS** — Russia's Progress MS-36 cargo ship is
   chasing the station today carrying Teledroid, its first humanoid
   robot; docking Thursday. Source: NASA Spaceflight.
9. **Three ships, two stations** — Shenzhou-24, Progress MS-36 and
   Northrop Grumman's Cygnus XL are all bound for orbit this week;
   Cygnus launches Sunday. Source: NASA.

## Deliberately left out (yesterday's news, 24 Nov — not shown)

The CIA/ODNI breach (first reported by the NYT on 24 Nov), the Houthi
strike on Riyadh's PIF tower (24 Nov, 11 wounded), Zelenskiy's
confirmation of the Sparta II strike (24 Nov), the Katz briefing on
Iranian chemical weapons (24 Nov), Putin's "retaliation inevitable"
warning (24 Nov), Iraq's Kurdish oilfield order (24 Nov), the Cartagena
supermarket hostage standoff (24 Nov), the WHO Ebola evacuation in
Congo (24 Nov), the BJP–SAD alliance (24 Nov), Sooryavanshi's record
204 (24 Nov), Anthropic falling below its $83 IPO price (24 Nov), the
Huawei guilty verdict (24 Nov), the Giuliani Medal of Freedom (24 Nov),
Dell raising its forecasts (24 Nov) and the Progress MS-36 launch
itself (24 Nov — the ship is shown only as in transit today).
