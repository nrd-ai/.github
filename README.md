# NotSquat · NRD AI

> **Equipment-utilization software and movement intelligence for strength gyms.**  
> *"See how your equipment is really being used."*

Welcome to the **NRD AI** organization workspace. This hub coordinates product architecture, mobile client engineering, computer-vision models, data warehouse pipelines, and founding partner programs for NotSquat.

---

## 🧭 Repository Radar

| Repository | Purpose | Tech Stack | Primary Focus |
|---|---|---|---|
| [`Not-Squat`](https://github.com/nrd-ai/Not-Squat) | **Central Hub & Platform Core** — Brand strategy, business architecture, backend specifications, and asset storage | Python, Fastify/Node, Markdown | Business readiness, agent fleet contracts, canonical screenshot archive |
| [`notsquat-mobile-app`](https://github.com/nrd-ai/notsquat-mobile-app) | **Mobile Application Client** — Real-time on-device workout capture, Gymtar RPG avatar progression, and gym circle feeds | Flutter, Dart, Riverpod, Google ML Kit | Hands-free mixed exercise capture validation (`/session`), avatar customization |
| [`notsquat-marketing-site`](https://github.com/nrd-ai/notsquat-marketing-site) | **Partner & Marketing Web Suite** — Founding-gym partner one-pager, operator deck, and web showcase | Modern HTML5, CSS3, Vanilla JS | Founding-gym design partner applications, live athletic editorial layouts |
| [`NotSquat-Data-Warehouse`](https://github.com/nrd-ai/NotSquat-Data-Warehouse) | **Telemetry & Analytics Warehouse** — Session metrics, aggregated equipment occupancy, and warehouse models | BigQuery, dbt, SQL, Python | Privacy-preserving aggregate station utilization analytics |
| [`Not-Squat-Detector-v0`](https://github.com/nrd-ai/Not-Squat-Detector-v0) | **CV Research Prototype** — Experimental computer vision pipelines for barbell & rep kinematics | Python, OpenCV, MediaPipe | Kinematic angle calculation, barbell velocity, and occlusion recovery |
| [`org-discord`](https://github.com/nrd-ai/org-discord) | **Team Agent Integrations** — Portable REST-only agent skill for company Discord collaboration | Python, REST API | Safe allowlisted channel telemetry and agent announcements |

---

## ⚡ Active Workstreams & Member Updates

### 1. 📱 Mobile App Capture Validation (`nrd-ai/notsquat-mobile-app`)
- **Hands-Free Scanning Flow:** Transitioned capture activation to readiness-gated `Start scanning` with automatic squat vs. jumping jack classification.
- **On-Device Inference:** Google ML Kit pose detection integrated natively on iOS and Android without cloud frame streaming.
- **Gymtar Studio & Raid Campaigns:** Integrated 16-bit pixel character progression, XP curves, campaign boss raids (Grip Ghost, Chalk Wraith), and attribute radar charts.

### 2. 🏛️ Founding Partner Gym Rollout (`nrd-ai/notsquat-marketing-site`)
- **Design Partnership Offer:** No-cost collaborative pilot program for independent strength and bodybuilding gyms.
- **Real Build Showcases:** Replaced legacy concept mocks with authentic iOS simulator and device screenshots across all partner decks and one-pagers.
- **Email Signature Studio:** Added official dark/light HTML email signature generator for team outreach.

### 3. 📊 Analytics & Privacy Infrastructure (`nrd-ai/NotSquat-Data-Warehouse`)
- **Equipment-Centered Metrics:** Engineering pipeline to separate active lifting time from rest and idle station occupancy.
- **Privacy Boundaries:** Strict adherence to aggregate, de-identified reporting — zero persistent member surveillance or facial biometrics.

---

## 🛡️ Engineering & Brand Guardrails

1. **Claims Discipline:** Plans, working components, and validated results are strictly separated. Do not claim unverified accuracy, privacy compliance, or commercial outcomes in customer-facing materials without founder approval.
2. **Brand Source of Truth:** Review [`docs/BRAND_STRATEGY.md`](https://github.com/nrd-ai/Not-Squat/blob/main/docs/BRAND_STRATEGY.md) and [`docs/BUSINESS_READINESS.md`](https://github.com/nrd-ai/Not-Squat/blob/main/docs/BUSINESS_READINESS.md) before publishing positioning or visual changes.
3. **Clean Code & Reversibility:** Avoid committing debug overrides, temporary simulator routing hacks, or synthetic mockups.

---

## 👥 Quick Links for Members

- 📋 [NotSquat Main Repo Issues](https://github.com/nrd-ai/Not-Squat/issues)
- 🚀 [Mobile App PRs & Roadmap](https://github.com/nrd-ai/notsquat-mobile-app/pulls)
- 🎨 [Brand Strategy Guide](https://github.com/nrd-ai/Not-Squat/blob/main/docs/BRAND_STRATEGY.md)
- 💬 [Company Discord Skill](https://github.com/nrd-ai/org-discord)
