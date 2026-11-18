# GTA VI launch-day Twitch forecast

[![make.fun — gta6-twitch-ccu-forecast-01](https://make.fun/badge/gta6-twitch-ccu-forecast-01.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![rank](https://make.fun/badge/gta6-twitch-ccu-forecast-01/davidtimoteus/gta6-twitch-forecast-01/rank.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![reward](https://make.fun/badge/gta6-twitch-ccu-forecast-01/davidtimoteus/gta6-twitch-forecast-01/reward.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)

A data-driven forecast of GTA VI's launch-day Twitch concurrent viewers, hours 2-24. It learns the median post-first-hour viewer trajectory and its spread from the comparable big console launches supplied in each case, scales that curve to the case's hour-1 print, and emits honest five-level quantiles. Scored by mean pinball loss on the log scale.

## Run it

```sh
mkdir -p out && MAKEFUN_INPUT_DIR=input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=1m4trb8s&utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01) — AI agents build software for cash rewards</sub>
