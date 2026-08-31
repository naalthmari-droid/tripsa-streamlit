# TRIPSA — Saudi Route Intelligence

An elegant Streamlit app that plans optimized Saudi road trips — with distance, stay dates,
cost, readiness & local-impact scores — and enables **collaborative group planning** via a
short invite code (members join, set preferences, vote on destinations, and reach consensus).

## Features
- **Optimized routes** (TSP: nearest-neighbor + 2-opt) with per-stop stay dates
- **Two modes**: pick cities yourself, or use a **certified route**
- **Real data**: restaurants & attractions per city, matched to your **favorite cuisine**
- **Day scheduler** that respects your **wake/sleep hours** and pace
- **Group room**: invite code, member preferences, voting, **consensus score**, discussion
- **Interactive map** (Folium) drawing the optimized route
- **Readiness (0-100)** & **local economic impact** indicators
- SQLite persistence (trips, members, votes, comments)

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
Push to GitHub, then on share.streamlit.io pick this repo, branch `main`, file `app.py`.

## Files
- `app.py` — Streamlit UI (English, animated elegant theme)
- `engine.py` — route optimizer, day scheduler, consensus, invite codes
- `data.py` — destinations, restaurants, attractions, certified routes
- `db.py` — SQLite persistence
- `style.py` — custom CSS + animations
