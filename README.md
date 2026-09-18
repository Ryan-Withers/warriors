# Warriors 2026 draw

A single-page, no-build site showing the AFV 2026 Men's draw, with arrival
times, grounds and a subscribable calendar feed.

Live at **https://ryan-withers.github.io/warriors/** once GitHub Pages is
enabled (Settings → Pages → Source: *Deploy from a branch* → `main` / `/ (root)`).

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole site. Fixtures and venues live in the `#draw-data` JSON block near the top. |
| `warriors.ics` | The calendar feed people subscribe to. Must sit next to `index.html`. |
| `apple-touch-icon.png` | Home-screen icon on iOS. |
| `.nojekyll` | Tells Pages to serve the files as-is instead of running Jekyll. |

## Updating the draw

1. Edit the `#draw-data` JSON inside `index.html` (kickoff times, venues, duty team).
2. Open the page. It compares `warriors.ics` against what the new data produces
   and, if they differ, shows a notice with a **download the new warriors.ics**
   button.
3. Download it, replace `warriors.ics`, and commit both files together.

Keeping the two in step matters: anyone subscribed to the calendar gets
`warriors.ics`, not the page.
