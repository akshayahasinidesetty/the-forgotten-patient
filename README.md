# The Forgotten Patient — Hospital Flow Intelligence

A React + Vite prototype for hospital operations analytics. It includes a responsive dashboard, department comparisons, rule-based priority signals, patient-journey overview, diagnostic turnaround analysis, CSV import/export, and light/dark/night themes.

## Dataset and privacy

The provided archive contained `encounters.csv`, `departments.csv`, `diagnostic_tests.csv`, and `patients.csv`. This repository includes only **aggregated demonstration metrics** derived from the encounter, department, and diagnostic files in `src/data/demoData.json`. It deliberately does **not** include the raw patient CSV or patient identifiers.

CSV uploads are parsed locally in the browser in this prototype. Upload `encounters.csv` to calculate visit and wait-time summaries; optionally include `departments.csv` and `diagnostic_tests.csv`. Do not upload identifiable patient information to a public website or repository.

## Run locally

Requirements: Node.js 18+ recommended.

```bash
npm install
npm run dev
```

Open the local URL printed by Vite.

To create a production build:

```bash
npm run build
npm run preview
```

## GitHub Pages / deployment

You can push this repository to GitHub and deploy it through a static hosting provider such as Vercel or Netlify. For GitHub Pages with a project repository, configure Vite's `base` path to `/<repository-name>/` before building.

## Important prototype limitations

- The sign-in screen is a **local demo gate only**. It is not secure authentication and must not protect real patient data. Connect Supabase Auth or another identity provider and enforce authorization on a backend before production.
- The provided prototype uses rule-based alerts and descriptive analytics. It does not contain a trained wait-time prediction model. Do not describe predictions as live until a validated model and API are connected.
- Operational flags are not clinical decisions. Human review is required.
