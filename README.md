# Rowan IEEE website — redesign

Multi-page static rebuild of [rowanieee.org](https://rowanieee.org).
Plain HTML/CSS/JS (no framework). Deployed from this `site/` folder via `npm run deploy`.

## Pages

| File | Purpose |
|------|---------|
| `index.html` | Home |
| `about.html` | What is IEEE / Rowan IEEE / meeting info |
| `events.html` | General meetings, workshops, SAC 2026, ProfHacks 2026 |
| `projects.html` | Showcase — competitions, workshops, hackathon gallery |
| `team.html` | E-Board |
| `contact.html` | Contact form (EmailJS) + meeting info + social links |
| `css/style.css` | Shared design system |
| `js/main.js` | Mobile nav, active link, contact form |
| `images/` | Team headshots, event art, ProfHacks gallery |

## Local preview

From the repo root:

```bash
npm run dev
```

then open http://localhost:5173.

Or from this folder: `python3 -m http.server 8000`.

## Contact form

The contact form uses the club's existing EmailJS service (same IDs as the previous React site). No extra setup needed unless those keys rotate.

## Updating content

Edit the HTML directly. Team roster is in `team.html`. Photos live under `images/` — keep filenames lowercase-with-dashes when adding new ones.

`build.py` can regenerate about/events/projects/team/contact from shared header/footer blocks if you change shared markup; `index.html` is hand-written and untouched by it.

## Deploy

From the repo root:

```bash
npm run build    # copies site/ → dist/
npm run deploy   # publishes dist/ to GitHub Pages
```
