# TRIPSA — Saudi Route Intelligence
## Hackathon Pitch Deck (Tourism Development Fund Hackathon)

---

### Slide 1 — Title
**TRIPSA — Saudi Route Intelligence**
Tagline: *"Plan your Saudi road trip with intelligence."*
The smart layer that turns Saudi tourism content into living, optimized, group-friendly road-trip experiences.
Presented for the Tourism Development Fund (TDF) Hackathon.

---

### Slide 2 — The Problem
**Saudi tourism is booming, but trip planning is still fragmented and manual.**
- Saudi Arabia welcomed **29.3M inbound visitors (SAR 176.6B)** and **93.3M domestic tourists (SAR 127.1B)** in 2025 — already surpassing the Vision 2030 target for the third year.
- Yet planning a multi-city road trip is still done across scattered websites, spreadsheets and WhatsApp groups.
- Official content (Visit Saudi itineraries, certified routes) is **static** — readable pages, not dynamic, bookable, optimizable journeys.
- Group travel (the dominant domestic segment — families) has **no tool** to reconcile everyone's preferences.

---

### Slide 3 — The Gap (Why now)
**No one owns the "brain of the route" — the missing intelligence layer.**
- Saudi Tourism Authority: publishes itineraries (static guides).
- Ministry of Tourism: TourismX & Saudi MT serve **businesses and investors**, not the individual traveler.
- Result: a real, validated gap for a **traveler-facing route-intelligence engine** — exactly what TRIPSA fills.
- We complement the ecosystem rather than compete with it.

---

### Slide 4 — The Solution
**TRIPSA: an intelligent route engine for Saudi road trips.**
- Builds an **optimized route** between cities (TSP + 2-opt) with distance, drive time, cost and per-stop stay dates.
- Two modes: **"Pick cities myself"** (custom) or **"Use a certified route"** (STA-approved routes brought to life).
- A **group-planning room** per trip with a short shareable **invite code**.
- Personalized **recommendations** that learn from past trips and user ratings.

---

### Slide 5 — Key Features (1/2)
**Engineered for the traveler's real journey.**
- **Route optimization engine:** orders cities to minimize drive time; shows per-stop arrival/departure dates and nights.
- **Smart day scheduling:** plans each day around the traveler's wake/sleep hours and pace (relaxed / moderate / action-packed).
- **Real local data:** actual attractions and restaurants per city, matched to the traveler's **favorite cuisine** and accommodation type.
- **Interactive route map** (Folium) with numbered stops and the path between them.

---

### Slide 6 — Key Features (2/2)
**Built for groups — a first in the market.**
- **Collaborative planning room:** members join via invite code, enter preferences, vote on destinations.
- **Live group-consensus score** and a winning route that maximizes collective satisfaction.
- **Comments & discussion** per trip or per destination.
- **Personalized "For You" recommendations** with star ratings & reviews that feed back into the recommender.
- **Email notifications** on booking confirmation, member joins, and trip updates.

---

### Slide 7 — How it works (Architecture)
**A clean, modular, data-driven pipeline.**
- **Data layer:** destinations, attractions, restaurants, certified routes (SQLite; extensible to live APIs).
- **Engine layer:** TSP route optimizer, day scheduler, consensus scorer, recommender (taste profile + rating feedback loop).
- **App layer:** Streamlit UI (English), custom CSS animations, Lottie, interactive maps.
- **Persistence:** trips, members, preferences, votes, comments, ratings, notifications.
- Deployed live on Streamlit Cloud; code on GitHub.

---

### Slide 8 — Two audiences, one platform
**Tourist-facing simplicity + business/government intelligence.**
- **Tourists** see a clean, delightful planning experience (no business jargon).
- **Admins / partners** unlock a hidden **dashboard**: readiness (0-100), local economic impact, most-demanded and most-reviewed destinations, rating distribution.
- This dual model serves both the traveler and the Tourism Development Fund's decision-makers.

---

### Slide 9 — Impact & Alignment with Vision 2030
**TRIPSA extends stays, spreads spend, and empowers regions.**
- Optimized multi-city routes **increase trip length and geographic spread** of spending.
- **Local economic impact indicator** highlights how each route benefits local communities.
- Surfaces **certified routes** and lesser-known destinations, distributing tourism beyond the major hubs.
- Data analytics give the TDF and Ministry **actionable demand signals** (what travelers want, where).

---

### Slide 10 — Why we win
**A validated gap, a working product, and a clear data moat.**
- **Live, working MVP** — not a concept; judges can use it now.
- **Unique group-consensus planning** — culturally tailored to Saudi family/group travel.
- **Self-improving recommender** — ratings feed back to sharpen suggestions.
- **Complements** STA/Ministry tools instead of competing — a partner, not a rival.
- Built on **real 2025-2026 official tourism data**.

---

### Slide 11 — Roadmap & Ask
**From hackathon MVP to national route-intelligence layer.**
- Next: live Google Places/Directions data, Arabic UI, PDF itinerary export, mobile app.
- Integrate with the Ministry's developer portal and STA certified-route registry.
- **Ask:** pilot with TDF destinations, access to official route/POI data, and incubation in the growth track.
- *TRIPSA — the brain of the Saudi road trip.*
