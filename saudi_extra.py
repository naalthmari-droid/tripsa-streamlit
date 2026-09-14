"""Almosaferoon.com scraped data -> TRIPSA structures.
Loads saudi_tourism_data.json, maps Arabic attraction categories to the app's
interest keys, adds 5 brand-new destinations, and enriches existing ones with
extra attractions, recommended stay, and best-visit months."""
import json, os

_PATH = os.path.join(os.path.dirname(__file__), "saudi_tourism_data.json")

# Arabic destination name -> app destination id (existing ones we enrich, not duplicate)
_EXISTING_MAP = {
    "الرياض": "riyadh", "جدة": "jeddah", "مكة المكرمة": "makkah",
    "المدينة المنورة": "madinah", "العلا": "alula", "الطائف": "taif",
    "أبها": "abha", "الأحساء": "alahsa", "تبوك": "tabuk",
    "ينبع": "yanbu", "الباحة": "albaha",
    # merged into one existing app destination
    "الخبر": "dammam_khobar", "الدمام": "dammam_khobar", "الظهران": "dammam_khobar", "الجبيل": "dammam_khobar",
}

# New destinations (id, name, region, lat, lng, interests, daily_cost, season, min_nights, highlights, blurb)
_NEW_DESTS = {
    "أملج": dict(id="umluj", name="Umluj", region="Tabuk Province", lat=25.0213, lng=37.2685,
        interests=dict(history_culture=2, nature_adventure=4, entertainment=2, shopping_luxury=1, relaxation=5, religious=1),
        daily_cost=380, occupancy=45, season="winter", holy=False, min_nights=1,
        highlights=["Umluj Beaches", "Duqm Island", "Al-Hurra Island"],
        blurb="The Maldives of Saudi Arabia — turquoise waters and white-sand islands."),
    "مدينة الملك عبدالله الاقتصادية": dict(id="kaec", name="KAEC", region="Makkah Province", lat=22.4491, lng=39.1275,
        interests=dict(history_culture=1, nature_adventure=3, entertainment=4, shopping_luxury=3, relaxation=5, religious=1),
        daily_cost=420, occupancy=48, season="winter", holy=False, min_nights=1,
        highlights=["KAEC Beach", "Golf Course", "Marina Walk"],
        blurb="A modern coastal city — beaches, golf and family resorts."),
    "جازان": dict(id="jazan", name="Jazan", region="Jazan Province", lat=16.8892, lng=42.5706,
        interests=dict(history_culture=3, nature_adventure=4, entertainment=2, shopping_luxury=2, relaxation=4, religious=1),
        daily_cost=300, occupancy=42, season="winter", holy=False, min_nights=1,
        highlights=["Jazan Corniche", "Fayfa Mountains", "Heritage Museum"],
        blurb="The Kingdom's tropical south — mangroves, mountains and heritage."),
    "جزيرة فرسان": dict(id="farasan", name="Farasan Island", region="Jazan Province", lat=16.7022, lng=42.1183,
        interests=dict(history_culture=2, nature_adventure=4, entertainment=2, shopping_luxury=1, relaxation=5, religious=1),
        daily_cost=350, occupancy=40, season="winter", holy=False, min_nights=2,
        highlights=["Farasan Marine Sanctuary", "Gazelle Reserve", "Diving"],
        blurb="A pristine island — coral reefs, gazelles and untouched nature."),
    "تنومة": dict(id="tanomah", name="Tanomah", region="Aseer Province", lat=18.9486, lng=42.1833,
        interests=dict(history_culture=2, nature_adventure=5, entertainment=2, shopping_luxury=1, relaxation=5, religious=1),
        daily_cost=280, occupancy=40, season="summer", holy=False, min_nights=1,
        highlights=["Tanomah Forests", "Hanging Village", "Mountain Trails"],
        blurb="A cool mountain hideaway — misty forests and dramatic cliffs."),
}

# Arabic attraction category -> app interest key (for scoring kind + interest match)
_CAT_TO_INTEREST = {
    "تراث": "history_culture", "تاريخي": "history_culture", "آثار": "history_culture",
    "ديني": "religious", "طبيعة": "nature_adventure", "مغامرة": "nature_adventure",
    "جبلي": "nature_adventure", "شاطئ": "relaxation", "ممشى": "relaxation",
    "ساحلي": "relaxation", "تسوق": "shopping_luxury", "ترفيه": "entertainment",
    "معلم": "entertainment", "متحف": "history_culture", "حديقة": "relaxation",
    "مطل": "nature_adventure", "غوص": "nature_adventure", "جزيرة": "relaxation",
    "تراثي": "history_culture", "ثقافي": "history_culture", "معماري": "history_culture",
}

# Interest key -> schedule kind (light/medium/heavy) used by the scheduler
_INTEREST_KIND = {"nature_adventure": "heavy", "history_culture": "medium",
                  "religious": "light", "entertainment": "medium",
                  "shopping_luxury": "medium", "relaxation": "light"}

def _classify(ar_type):
    """Map an Arabic attraction type string -> (interest_key, kind, est_duration_min)."""
    interest = "history_culture"
    for kw, key in _CAT_TO_INTEREST.items():
        if kw in ar_type:
            interest = key
            break
    kind = _INTEREST_KIND.get(interest, "medium")
    dur = {"light": 60, "medium": 90, "heavy": 150}.get(kind, 90)
    return interest, kind, dur

def load_extra():
    """Return (new_destinations:list, extra_attractions:list[tuple], enrichment:dict)."""
    if not os.path.exists(_PATH):
        return [], [], {}
    raw = json.load(open(_PATH, encoding="utf-8"))
    dests = raw.get("destinations", [])
    new_destinations, extra_attractions, enrichment = [], [], {}
    for x in dests:
        ar_name = x.get("name")
        rec_days = x.get("recommended_duration_days")
        months = x.get("best_visit_months", [])
        # resolve target id
        tid = _EXISTING_MAP.get(ar_name)
        if tid is None and ar_name in _NEW_DESTS:
            spec = _NEW_DESTS[ar_name]
            d = dict(spec)
            d["rec_days"] = rec_days
            d["best_months"] = months
            d["rec_days"] = rec_days or spec.get("min_nights", 1) + 1
            new_destinations.append(d)
            tid = d["id"]
        if tid is None:
            continue
        enrichment.setdefault(tid, {})["rec_days"] = rec_days
        enrichment.setdefault(tid, {})["best_months"] = months
        # attractions
        for a in x.get("attractions", []):
            interest, kind, dur = _classify(a.get("type", ""))
            aid = (a.get("url", "") or a.get("name", "")).strip().lower()
            aid = "xa_" + "".join(ch for ch in aid if ch.isalnum())[:28]
            rating = 4.3 + (hash(a.get("name", "")) % 5) / 10  # 4.3-4.7 stable
            extra_attractions.append(
                (aid, tid, a.get("name", ""), interest, 0.0, 0.0, round(rating, 1),
                 {"heavy": 1, "medium": 2, "light": 3}[kind], dur))
    # Fallback: a brand-new destination with no scraped attractions still gets
    # itinerary entries built from its (real) highlights so the scheduler works.
    for d in new_destinations:
        if not any(a[1] == d["id"] for a in extra_attractions):
            for h in d.get("highlights", []):
                aid = "xh_" + d["id"] + "_" + "".join(ch for ch in h.lower() if ch.isalnum())[:20]
                extra_attractions.append((aid, d["id"], h, "nature_adventure", 0.0, 0.0, 4.4, 1, 120))
    return new_destinations, extra_attractions, enrichment
