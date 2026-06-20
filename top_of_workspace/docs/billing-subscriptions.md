# Cloud & subscription billing audit

**Audited:** 2026-06-16 via fish mail search (`~/.config/fish/fish.db`, ~3,714 messages, Mar 16–Jun 16 2026).

**Accounts synced:** `ken@seehart.com`, `kenseehart@gmail.com`, `ken@agi.green` (`ken@evolver.ai` configured but not syncing).

---

## Proposed cancel list

Cancel or let lapse **before next renewal**. Ordered by confidence and savings.

| Service | Cost | Renews ~ | Account | Annual saved | Rationale |
|---------|------|----------|---------|--------------|-----------|
| **Figma** | $20/mo | ~13th | `kenseehart@gmail.com` | **$240** | **cristopoly** wraps in ~1 month; no other workspace project uses Figma. **Do not renew beyond June 2026** — cancel before July charge. Export/duplicate Cristopoly file first. |
| **Google AI Pro** (5 TB) | $19.99/mo | ~10th | `kenseehart@gmail.com` | **~$240** | No Gemini/One usage in repos. Overlaps Anthropic API + Cursor (+ ChatGPT Plus if active). Keep separate **Maps API** billing for cristopoly geocoding — that is not this subscription. |
| **Zoom Pro** | $16.99/mo | ~26th | `ken@seehart.com` | **~$204** | Zero meeting invites in synced mail; no video/meeting integrations in any project. |
| **Hugging Face Pro** | $9/mo | ~2nd | `ken@seehart.com` | **$108** | No `huggingface` / `hf_hub` / `transformers` in active project code. daime uses faster-whisper; fish uses OpenAI embeddings. |
| **Midjourney Basic** | $96/yr | ~May 30 | `ken@seehart.com` | **$96** | Active in Discord socially, but cristopoly is Figma + Street View + Claude — no generative art pipeline in repos. |
| **ChatGPT Plus** | ~$20/mo | unknown | `ken@seehart.com` (likely) | **Keeping** — phone image gen/OCR; cancel when Claude has image tools |
| **Windscribe VPN** *(optional)* | $8.99/mo | ~15th | `kenseehart@gmail.com` | **~$108** | No VPN references in workspace. Personal habit only. |
| **Lambda Cloud** | — | — | — | — | **Close dormant storage** (US-SOUTH-1 migration emails Apr–May). Not a recurring sub in mail; workspace uses GCP + RunPod. |

### Cancel-list savings

| Scope | Annual |
|-------|--------|
| **Confirmed subs in mail** (Figma + Google AI Pro + Zoom + HF Pro + Midjourney) | **~$888/yr** (~$74/mo) |
| **+ ChatGPT Plus** (if active) | **~$1,128/yr** |
| **+ Windscribe** (if dropped) | **~$1,236/yr** |

### Keep (project-backed)

| Service | Cost | Why keep |
|---------|------|----------|
| **Anthropic API** | $20/mo | daime agents, nfnc policy, general agent work (`ken@agi.green`) |
| **OpenAI API** | usage-based | fish embeddings/topics, daime fallback, PRISM labels |
| **GCP** (`upscale-vm`) | usage-based | daime GPU (ASR, Demucs, alignment) via `compute daime-gpu` |
| **hosting.com** | ~$30/yr | `yknotlabs.com` domain — Game of Y deploys to `yknotlabs.com/gameofy/` |
| **Cursor Pro** | ~$20/mo *(unconfirmed in mail)* | Primary coding agent; keep if subscribed |

### Usage habits (not subscriptions)

| Item | Action |
|------|--------|
| **GCP VM left running** | `compute down daime-gpu` when idle — explains $8 vs $50 month-to-month |
| **OpenAI API auto-reload** | Lower threshold if spend is higher than needed |

---

## All services found in mail

### Fixed recurring (confirmed receipts)

| Service | Amount | Frequency | Account |
|---------|--------|-----------|---------|
| Anthropic API | $20.00 | Monthly (~26th) | `ken@agi.green` |
| Hugging Face Pro | $9.00 | Monthly (~2nd) | `ken@seehart.com` |
| Google AI Pro (Google One 5 TB) | $19.99 | Monthly (~10th) | `kenseehart@gmail.com` |
| Figma | $20.00 | Monthly (~13th) | `kenseehart@gmail.com` |
| Midjourney | $96.00 | Annual (receipt May 30) | `ken@seehart.com` |
| hosting.com (yknotlabs.com) | $29.94 | Annual domain | Jeff Mallett account; Ken pays |
| Windscribe Pro | $8.99 | Monthly (~15th) | `kenseehart@gmail.com` (Google Play) |
| Zoom | $16.99 | Monthly (~26th) | `ken@seehart.com` |

### Variable / usage-based

| Service | Evidence (Mar–Jun 2026) | Account |
|---------|-------------------------|---------|
| **OpenAI API** | Auto-fund $10 (May 7) + $40 (May 29) = $50 total | `ken@seehart.com` |
| **GCP** (`upscale-vm`) | $31.06 (Apr), $50.46 (May), $8.47 (Jun) | `kenseehart@gmail.com`, Visa ••••5250 |
| **Google Maps API** | Pay-per-use for cristopoly Street View/geocoding (not a flat sub) | GCP API key |
| **GitHub Copilot** | Usage-based billing notice (Apr 27); no charge amounts in mail | `ken@seehart.com` |
| **Meshy** | One $6 receipt (Jun 15); not clearly recurring | `kenseehart@gmail.com` |

### Mentioned but no billing receipts

| Service | Notes |
|---------|-------|
| **RunPod** | Marketing only; provider implemented in `compute/` but no charge emails |
| **Lambda Cloud** | Storage migration notices (US-SOUTH-1); no payment amounts |
| **AWS / Azure / MongoDB Atlas** | Nothing in synced mail |
| **Cursor Pro** | Upsell emails only; no Stripe receipts |

---

## Annual totals

### Fixed only (excluding usage-based)

| Item | Annual |
|------|--------|
| Anthropic API | $240 |
| Hugging Face Pro | $108 |
| Google AI Pro | ~$240 |
| Figma | $240 |
| Midjourney | $96 |
| hosting.com | ~$30 |
| **Subtotal — all fixed in mail** | **~$954/yr** (~$79/mo) |

### After proposed cancels (keep Anthropic + hosting)

| Item | Annual |
|------|--------|
| Anthropic API | $240 |
| hosting.com | ~$30 |
| **Remaining fixed** | **~$270/yr** (~$23/mo) |

### Variable (not “cancel” — manage usage)

| Service | Annual estimate |
|---------|-----------------|
| GCP (`upscale-vm`) | $96–600 (3-mo avg ~$360) |
| OpenAI API | ~$200–600 |

---

## Workspace coverage by project

What each project actually consumes vs. cancellation candidates.

| Project | Active paid deps | Cancellation candidates useful? |
|---------|------------------|--------------------------------|
| **daime** | GCP GPU (`compute daime-gpu`), Anthropic/OpenAI API | **No** — faster-whisper on VM, not HF Pro or Gemini |
| **fish** | OpenAI API; future PRISM on RunPod (`prism-train`) | **No** — OpenAI embeddings, not HF |
| **cristopoly** | Figma (ending), Maps API, Cursor/Claude | **Figma → cancel after June**; Midjourney/Meshy not in workflow |
| **compute** | GCP + RunPod | **Lambda** orphaned |
| **upscale** | Shares GCP `daime-gpu` | **No** |
| **y** | Static hosting via `host` / yknotlabs.com | **No** |
| **host / seehart** | hosting.com static deploy | **No** |
| **tesla / nfnc** | Tesla API, Google Sheets OAuth | **No** |
| **agi.green** | Legacy reference only | **No** |

### Existing stack (covers project needs)

| Need | Tool |
|------|------|
| Coding agents | Cursor |
| LLM agents | Anthropic API (+ OpenAI fallback) |
| Email RAG + PRISM | OpenAI API |
| GPU ASR / stems / alignment | GCP `upscale-vm` |
| PRISM training (planned) | RunPod CPU (`prism-train`) |
| Board art (cristopoly, until done) | Figma |
| Property imagery | Google Maps API (pay-per-use) |
| 3D game pieces | STL assets (`cristopoly/src/cristopoly/hollow_pieces.py`) |

---

## Per-candidate detail

### Figma — **cancel after June 2026**

- **Receipt:** $20/mo, `kenseehart@gmail.com`, renews ~13th (last receipt Jun 13, 2026).
- **Workspace use:** **cristopoly** only — board art, cards, print exports (`cristopoly/AGENTS.md`). Figma MCP in Cursor for edits.
- **Status:** Project ~done within a month; no renewal needed beyond June.
- **Before cancel:** Duplicate Cristopoly file; export final print assets (500×500 mm board, A4 cards per AGENTS.md).
- **After cancel:** Read-only access to duplicated file may remain on free tier; MCP edits require paid seat.

### Hugging Face Pro — **cancel**

- **Receipt:** $9/mo, `ken@seehart.com`.
- **Workspace use:** None in active code. Archived `archive_from_evolver/daime/` Qwen3 ASR used `from_pretrained` — replaced by faster-whisper.
- **Theoretical future:** fish PRISM on open embeddings (e5, BGE) would use free Hub tier for public models; Pro not required.

### Google AI Pro (Gemini + 5 TB) — **cancel**

- **Receipt:** $19.99/mo, `kenseehart@gmail.com` (PayPal → `ken@seehart.com`).
- **Product:** “Google AI Pro (5 TB) (Google One)”.
- **Workspace use:** No Gemini/Vertex in code. cristopoly uses **Maps API** (separate GCP billing). nfnc uses Sheets OAuth (standard Google Cloud).
- **Theoretical future:** Personal backup of daime `data/` to Drive — not integrated in repos.

### Zoom Pro — **cancel**

- **Receipt:** $16.99/mo, `ken@seehart.com`.
- **Workspace use:** None. “Zoom” in cristopoly = map tile zoom.

### Midjourney Basic — **cancel** (unless keeping for hobby)

- **Receipt:** $96/yr (May 30), likely annual Basic plan.
- **Workspace use:** None in repos. Discord/community activity present but not tied to project workflows.

### ChatGPT Plus — **cancel if subscribed**

- **Mail:** Product emails only; no payment receipts in fish window.
- **Workspace use:** Redundant — fish/daime/PRISM use OpenAI **API**; coding via Cursor; content via Anthropic.

### Windscribe VPN — **cancel** (personal only)

- **Receipt:** $8.99/mo via Google Play, `kenseehart@gmail.com`.
- **Workspace use:** None.

### Lambda Cloud — **close dormant account**

- **Mail:** US-SOUTH-1 filesystem/storage migration (Apr–May 2026).
- **Workspace use:** Superseded by `compute/resources.yaml` (GCP `daime-gpu`, RunPod `prism-train` / `daime-gpu-runpod`).

### Services to keep

**Anthropic API** — $20/mo on `ken@agi.green`; monthly receipts Mar–Jun. Core to daime LLM agents and agent work.

**OpenAI API** — Usage-based auto-reload on `ken@seehart.com`. fish embeddings (`fish/src/fish/embed.py`), topics, PRISM training labels (`prism_whitepaper.md`).

**GCP** — VM `upscale-vm` (T4) for daime; referenced in `compute/resources.yaml` and `daime/AGENTS.md`. Variable cost; stop VM when idle.

**hosting.com** — `yknotlabs.com` domain renewal $29.94/yr (Jeff Mallett account). Game of Y: `y/AGENTS.md`, deploy to `yknotlabs.com/gameofy/`.

---

## Gaps & limitations

1. **90-day mail window** — fish sync may miss older annual renewals or quiet services.
2. **Duplicate messages** — Gmail INBOX + All Mail synced (~2× for some receipts).
3. **`ken@evolver.ai`** — not syncing (auth timeout).
4. **Cursor / ChatGPT Plus** — ChatGPT Plus likely active (`ken@seehart.com` product email, no payment receipt). Cursor likely **free tier** (upsell Jun 13, no payment receipt). Verify at chatgpt.com / cursor.com settings.
5. **seehart.com hosting** — hosting.com login on `ken@seehart.com`; no separate invoice in this window (may be under same or different account).

---

## Action checklist

- [ ] **Figma:** finish cristopoly exports; duplicate file; cancel before **July 13, 2026**
- [x] **Google AI Pro / Windscribe / Termius / Plura:** canceled (user, 2026-06-18)
- [x] **Zoom:** canceled (user, 2026-06-18)
- [x] **Midjourney:** canceled (user, 2026-06-18)
- [ ] **ChatGPT Plus:** **keeping for now** — phone image sketching/OCR; cancel after Claude image gen integrated (reminder below)
- [ ] **GCP:** `compute down daime-gpu` when not training/transcribing
- [ ] **OpenAI API:** review auto-reload amount in platform dashboard

---

## Cancellation log

| Service | Status | Effective end | Confirmation | Notes |
|---------|--------|---------------|--------------|-------|
| **Lambda Cloud** | **Closed** | 2026-06-18 | — (user) | No workspace use; GCP + RunPod |
| **Hugging Face Pro** | **Canceled** | ~Jul 2, 2026 (paid through) | — (user) | Free tier sufficient for Hub downloads + own GPU |
| **Google AI Pro** | **Canceled** | Jul 10, 2026 | Play `SOP.3357-9970-3690-58362` | User 2026-06-18. Maps API separate (GCP) |
| **Windscribe Pro** | **Canceled** | Jul 15, 2026 | Play `GPA.3376-1383-2658-25337` | User 2026-06-18 |
| **Termius Pro** | **Canceled** | Sep 12, 2026 | — | User 2026-06-18. Use `compute ssh` |
| **Plura+** | **Canceled** | Oct 22, 2026 | — | User 2026-06-18. Personal |
| **Zoom Pro** | **Canceled** | ~Jul 26, 2026 | Account `50448904` | User 2026-06-18 |
| **Midjourney Basic** | **Canceled** | May 30, 2027 (paid through) | Receipt `#2237-4631-2889` | User 2026-06-18 |
| **Figma** | Pending manual | Jul 13, 2026 (paid through) | Invoice `in_1Ti1JSIvcqWR3dFDaB4NJhTv` | **Export Cristopoly first** |
| **ChatGPT Plus** | **Keep (for now)** | — | Product email May 18 | **$20/mo** — image gen + OCR on phone app; Midjourney canceled. **Cancel when:** Claude app has integrated image generation (see reminder below) |

### Verification (2026-06-18)

| Service | Finding |
|---------|---------|
| **Cursor Pro** | Upsell Jun 13; no payment receipt in fish. **Do not cancel** — primary IDE. |
| **ChatGPT Plus** | **Keep** (user decision 2026-06-18). Image gen + OCR on phone; replaces Midjourney for casual sketches. Claude chat weak on SVG/line art; Cursor can generate images but not the mobile ChatGPT UX. **Cancel trigger:** integrated image gen in Claude app (OAuth MCP or hosting tool calling DALL·E / similar). |
| **Google Maps API** | **Separate from Google AI Pro.** Maps uses `GOOGLE_MAPS_API_KEY` in a GCP project (`cristopoly/.env`); pay-per-use billed to payments profile `2694-5921-7491` (Visa ••••5250). Google AI Pro is a Google Play / Google One subscription on `kenseehart@gmail.com` (PayPal `ken@seehart.com`). Canceling Google AI Pro does **not** affect geocoding or Street View. |

### Reminder: cancel ChatGPT Plus

**When:** Claude mobile (or a workspace MCP you use daily) can generate and interpret images at least as well as the ChatGPT app for your sketching workflow.

**Likely integration paths** (pick one when ready):

1. **MCP image tool on hosting.com** — FastMCP tool wrapping OpenAI `dall-e-3` or similar; callable from Claude connector (same pattern as Tesla/fish).
2. **OpenAI API direct** — you already pay usage-based; expose via a thin `host` or `shared` CLI/MCP rather than $20/mo chat sub.
3. **Cursor** — already capable (see `cristina-watercolor-portrait.png`); good for desktop, not phone.

**Action:** Revisit when fish or host MCP deploy is stable; search billing doc for "ChatGPT Plus" and cancel at [chatgpt.com](https://chatgpt.com) → Settings → Subscription. Saves **~$240/yr**.

---

## Billing portal click paths

Use these direct URLs. Sign in with the account shown.

### 1. Figma — `kenseehart@gmail.com` — cancel before Jul 13

**Before canceling:**

1. Duplicate the Cristopoly Figma file (File → Save as copy / duplicate to your drafts).
2. Export final print assets per `cristopoly/AGENTS.md`:
   - Board: 500×500 mm from **Variable Template → Board**
   - Cards: **Variable Cards - A4** deed/action sheets
   - Use `download_assets` MCP or Figma export for PNG/PDF proofs

**Cancel path:**

1. [figma.com](https://www.figma.com) → sign in as `kenseehart@gmail.com`
2. Team **Ken Seehart's team** → **Admin** (gear) → **Billing**
3. **Cancel plan** (Settings tab) — downgrades at end of period (Jul 13, 2026)
4. Alt: [figma.com/settings](https://www.figma.com/settings) → team billing

Last receipt: $20/mo, period Jun 13–Jul 13, 2026. Invoice `in_1Ti1JSIvcqWR3dFDaB4NJhTv`.

### 2. Google AI Pro — `kenseehart@gmail.com` — cancel before Jul 10

1. [play.google.com/store/account/subscriptions](https://play.google.com/store/account/subscriptions) (signed in as `kenseehart@gmail.com`)
2. **Google AI Pro (5 TB) (Google One)** → **Cancel subscription**
3. Confirm — access continues until Jul 10 billing cycle ends

Order `SOP.3357-9970-3690-58362`, $19.99/mo, PayPal `ken@seehart.com`.

**Maps API safe:** GCP console billing (`2694-5921-7491`) is independent. Verify at [console.cloud.google.com/billing](https://console.cloud.google.com/billing) — Geocoding / Street View / Maps Static APIs stay enabled on your API key.

### 3. Zoom Pro — `ken@seehart.com` — cancel before Jul 26

1. [zoom.us/billing](https://zoom.us/billing) or [zoom.us/account/billing](https://zoom.us/account/billing)
2. Sign in → **Plans and Billing** → **Cancel Subscription** (or downgrade to Basic)
3. Account number **50448904**, $16.99/mo via PayPal

### 4. Hugging Face Pro — `ken@seehart.com` — cancel before Jul 2

1. [huggingface.co/settings/billing](https://huggingface.co/settings/billing)
2. **Manage subscription** → **Cancel** (Stripe portal)
3. Receipt `#2194-3867`, $9/mo, period Jun 1–Jun 30, 2026

### 5. Midjourney Basic — `ken@seehart.com` — annual, renews May 30, 2027

1. [billing.midjourney.com/p/login/aEUdRA5Wc8t25a03cc](https://billing.midjourney.com/p/login/aEUdRA5Wc8t25a03cc) (magic link to `ken@seehart.com`)
2. **Cancel subscription** — or let lapse until May 2027 (already paid $96 through May 30, 2027)
3. Alt: Discord → Midjourney Bot → `/subscribe` → manage

Receipt `#2237-4631-2889`, Basic Plan $96/yr.

### 6. ChatGPT Plus — verify then cancel if active

1. [chatgpt.com](https://chatgpt.com) → sign in (`ken@seehart.com` likely)
2. Profile → **Settings** → **Subscription** → **Manage** / **Cancel**
3. Alt billing portal: [pay.openai.com](https://pay.openai.com)

**Fish finding:** product emails reference ChatGPT Plus; no Plus payment receipt (API funding receipts are separate). Check Settings before canceling.

### 7. Windscribe Pro — `kenseehart@gmail.com` — cancel before Jul 15

1. [play.google.com/store/account/subscriptions](https://play.google.com/store/account/subscriptions)
2. **Windscribe Pro** → **Cancel subscription**

Order `GPA.3376-1383-2658-25337`, $8.99/mo, PayPal `ken@seehart.com`.

### 7b. Termius Pro — `kenseehart@gmail.com` — cancel before Sep 12

1. Same Play subscriptions page → **Termius Pro** → **Cancel subscription**
2. $120/yr. Workspace SSH uses `compute ssh daime-gpu` / `gcloud compute ssh` — Termius Pro not required.

### 7c. Plura+ — `kenseehart@gmail.com` — cancel before Oct 22

1. Same Play subscriptions page → **Plura+** → **Cancel subscription**
2. $71.99/yr. Personal app; no workspace dependency.

### 8. Lambda Cloud — close dormant US-SOUTH-1 storage

1. [cloud.lambdalabs.com](https://cloud.lambdalabs.com) → sign in (`ken@agi.green` received migration mail)
2. Check **Filesystems** in US-SOUTH-1 — delete if empty/unneeded
3. If data remains: [support.lambda.ai](https://support.lambda.ai) → ticket for CPU migration slot (**deadline Jun 19, 2026** per Apr 29 notice)

Not a recurring subscription; no payment receipts in mail.

### Do NOT cancel

| Service | Portal | Reason |
|---------|--------|--------|
| Anthropic API | [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing) | daime, nfnc, agent work |
| OpenAI API | [platform.openai.com/settings/organization/billing](https://platform.openai.com/settings/organization/billing) | fish embeddings, daime fallback |
| GCP (`upscale-vm`) | [console.cloud.google.com/billing](https://console.cloud.google.com/billing) | daime GPU |
| hosting.com | hosting.com account (Jeff Mallett) | `yknotlabs.com` domain |
| Cursor Pro | [cursor.com/settings](https://cursor.com/settings) | Primary IDE — keep if active |

---

## Re-audit

```bash
fish sync --days 365          # extend history
fish search "receipt invoice payment billing subscription"
```

Update this doc when subscriptions change.
