# news-image-20261127-v2

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/tpmtling/news-image-20261127-v2/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/tpmtling/news-image-20261127-v2/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

THE WORLD TODAY — a one-page newspaper front page summing up 27 November 2026's world news in a single image. Lead story: a Thanksgiving storm cuts power and grounds flights on the US East Coast. Also inside: Kim Jong Un orders North Korea's nuclear programme to expand, Iran says three tankers hit mines in the Strait of Hormuz, UK net migration falls to 77,000 — its lowest since 1997 — Spain's Hernandez de Cos is named the next ECB chief, all hostages are freed after a 16-hour supermarket siege in Colombia, and Hong Kong marks a year since its deadly high-rise fire. The entry is rendered offline with Pillow (`render.py`); `main.py` is standard library only and copies the pre-rendered `entry.png` to the output directory, so it runs in the scorer's python:3.13-slim image.

## Run it

```sh
python3 render.py   # draws entry.png (needs Pillow, local only)
python3 main.py     # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=fpwjs2j2&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>
