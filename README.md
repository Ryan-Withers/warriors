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
| `manifest.webmanifest` | Web app manifest, so Android installs it like an app too. |
| `apple-touch-icon.png` | Home-screen icon on iOS. 180x180, no transparency. |
| `icon-192.png`, `icon-512.png` | Manifest icons. |
| `icon-maskable-512.png` | Manifest icon with safe-zone padding for Android's adaptive mask. |
| `share-card.png` | The 1200x630 image link previews show. |
| `.nojekyll` | Tells Pages to serve the files as-is instead of running Jekyll. |

## Updating the draw

1. Edit the `#draw-data` JSON inside `index.html` (kickoff times, venues, duty team).
2. Open the page. It compares `warriors.ics` against what the new data produces
   and, if they differ, shows a notice with a **download the new warriors.ics**
   button.
3. Download it, replace `warriors.ics`, and commit both files together.

Keeping the two in step matters: anyone subscribed to the calendar gets
`warriors.ics`, not the page.

## Regenerating the images

`apple-touch-icon.png` is the source of truth for every icon. If the club logo
changes, replace it (180x180, no alpha, flat background) and run
`python3 tools/make-images.py` to rebuild the manifest icons and the share card.

## Getting to the ground

Every venue offers Waze, Apple Maps and Google Maps, and all three **start
navigating** rather than dropping a pin, so whichever one someone picks behaves
the same way:

| App | Link |
| --- | --- |
| Waze | `https://waze.com/ul?q=<ground, address>&navigate=yes` |
| Apple Maps | `https://maps.apple.com/?daddr=<ground, address>&dirflg=d` |
| Google Maps | `https://www.google.com/maps/dir/?api=1&destination=<ground, address>` |

Waze's `/ul` is a universal link: it hands off to the app when installed and falls
back to waze.com when not.

The rows list every app except one already named by a control beside them, which
is why the next-game card shows only Apple and Google under its own **Go with
Waze** button. The venue name on each fixture is itself a Waze link, as a larger
tap target than the row.

## Subscribing, per platform

There is no single link that subscribes everywhere, so the page picks a route
from the user agent and offers the rest as alternatives.

| Platform | Main button | Also offered |
| --- | --- | --- |
| iOS, iPadOS, macOS | Apple Calendar, `webcal://` | Google Calendar, Outlook, Copy link |
| Android | Google Calendar | Outlook, Copy link |
| Windows, Linux | Google Calendar | Outlook, Apple Calendar, Copy link |

Two things drive that table:

- **`webcal://` has no registered handler on Android.** A `webcal://` link there
  opens nothing at all, in Chrome, Samsung Internet and Firefox alike, so Android
  is never offered one. It stays on Apple and desktop, where a local calendar
  client picks it up.
- **Google Calendar cannot add a subscription from a phone.** Neither its Android
  nor its iOS app has an add-by-URL screen, and the mobile web redirects away from
  the one that exists. The link works on a computer, and the subscription then
  syncs down to the phone, so Android users get a line saying exactly that rather
  than a button that looks broken.

Copy link is the universal fallback and is always present.

## Link previews and the home screen

Absolute URLs in the `og:` tags point at `https://ryan-withers.github.io/warriors/`.
If the site ever moves to another address, those tags and `share-card.png`'s URL
have to move with it, because WhatsApp and iMessage do not resolve relative ones.

Opening the page from inside another app, WhatsApp especially, runs it in a
WebView that blocks calendar downloads. The page detects that and says to open
it in Safari rather than letting the buttons fail quietly.
