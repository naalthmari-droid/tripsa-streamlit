"""TRIPSA — Core engine: route optimization, day scheduling, consensus, invite codes."""
import math
import random
import string
from datetime import datetime, timedelta

from data import DEST_BY_ID, attractions_for, restaurants_by_cuisines

AVG_SPEED_KMH = 90.0

# ----------------------------- Transport modes -----------------------------
# Each mode: label, icon, average speed (km/h), fixed overhead (min per leg).
TRANSPORT_MODES = {
    "road":  {"label": "By road",  "icon": "🚗", "speed": 90.0,  "overhead_min": 0},
    "air":   {"label": "By air",   "icon": "✈️", "speed": 700.0, "overhead_min": 120},
    "rail":  {"label": "By rail",  "icon": "🚄", "speed": 160.0, "overhead_min": 30},
}


def travel_minutes(km, mode="road"):
    """Travel time for a leg given the transport mode (includes overhead)."""
    m = TRANSPORT_MODES.get(mode, TRANSPORT_MODES["road"])
    return int(round((km / m["speed"]) * 60)) + m["overhead_min"]


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def drive_minutes(km):
    return int(round((km / AVG_SPEED_KMH) * 60))


def destination_score(dest, interests):
    s, w = 0.0, 0.0
    for k, v in interests.items():
        s += dest["interests"].get(k, 0) * v
        w += v
    return (s / (w * 5)) if w else 0.0


def rank_destinations(interests, include_holy, exclude_ids=None, limit=6):
    exclude_ids = exclude_ids or []
    scored = []
    for d in DEST_BY_ID.values():
        if d["holy"] and not include_holy:
            continue
        if d["id"] in exclude_ids:
            continue
        scored.append((destination_score(d, interests), d))
    scored.sort(key=lambda x: -x[0])
    return [d for _, d in scored[:limit]]


def readiness_score(dest):
    occ = dest["occupancy"]
    return max(0, min(100, round(100 - abs(occ - 70) * 1.2)))


def local_impact_score(dest):
    base = 100 - (dest["daily_cost"] / 700) * 40
    return max(30, min(95, round(base)))


def _nearest_neighbor_order(start_id, ids):
    remaining = list(ids)
    order = []
    cur = start_id
    while remaining:
        nxt = min(remaining, key=lambda x: haversine_km(
            DEST_BY_ID[cur]["lat"], DEST_BY_ID[cur]["lng"],
            DEST_BY_ID[x]["lat"], DEST_BY_ID[x]["lng"]))
        order.append(nxt)
        remaining.remove(nxt)
        cur = nxt
    return order


def _route_distance(order):
    total = 0.0
    for i in range(1, len(order)):
        a, b = DEST_BY_ID[order[i - 1]], DEST_BY_ID[order[i]]
        total += haversine_km(a["lat"], a["lng"], b["lat"], b["lng"])
    return total


def _two_opt(order):
    best = list(order)
    best_d = _route_distance(best)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 1):
            for j in range(i + 1, len(best)):
                cand = best[:i] + best[i:j + 1][::-1] + best[j + 1:]
                d = _route_distance(cand)
                if d < best_d - 1e-6:
                    best, best_d = cand, d
                    improved = True
    return best


def season_from_date(dt):
    m = dt.month
    return "summer" if m in (5, 6, 7, 8, 9) else "winter"


def build_optimized_route(start_id, dest_ids, interests, start_date, end_date,
                          travelers, budget_daily, pace, include_holy, transport_mode="road"):
    """Build an optimized multi-stop route with per-stop stay dates."""
    nights_total = max(1, (end_date - start_date).days)
    if not dest_ids:
        ranked = rank_destinations(interests, include_holy, exclude_ids=[start_id], limit=6)
        dest_ids = [d["id"] for d in ranked]
    dest_ids = [d for d in dest_ids if d != start_id and (include_holy or not DEST_BY_ID[d]["holy"])]

    order = _two_opt(_nearest_neighbor_order(start_id, dest_ids)) if len(dest_ids) > 1 else dest_ids
    full_order = [start_id] + order

    # allocate nights proportional to min_nights
    weights = [DEST_BY_ID[x]["min_nights"] for x in full_order]
    wsum = sum(weights) or 1
    nights = [max(1, round(nights_total * w / wsum)) for w in weights]
    # adjust to match total nights
    diff = nights_total - sum(nights)
    i = 0
    while diff != 0 and nights:
        idx = i % len(nights)
        if diff > 0:
            nights[idx] += 1
            diff -= 1
        elif nights[idx] > 1:
            nights[idx] -= 1
            diff += 1
        i += 1
        if i > 1000:
            break

    stops = []
    cur = start_date
    total_km = 0.0
    total_min = 0
    total_cost = 0.0
    for idx, did in enumerate(full_order):
        d = DEST_BY_ID[did]
        n = nights[idx]
        check_in = cur
        check_out = cur + timedelta(days=n)
        if idx == 0:
            dist_prev, dmin = 0.0, 0
        else:
            prev = DEST_BY_ID[full_order[idx - 1]]
            dist_prev = haversine_km(prev["lat"], prev["lng"], d["lat"], d["lng"])
            dmin = travel_minutes(dist_prev, transport_mode)
        total_km += dist_prev
        total_min += dmin
        total_cost += d["daily_cost"] * n * travelers
        stops.append(dict(
            destination_id=did, name=d["name"], order=idx + 1, nights=n,
            check_in=check_in.isoformat(), check_out=check_out.isoformat(),
            distance_from_prev_km=round(dist_prev, 1), drive_min=dmin,
            highlights=d["highlights"], daily_cost=d["daily_cost"],
            lat=d["lat"], lng=d["lng"],
        ))
        cur = check_out

    readiness = round(sum(readiness_score(DEST_BY_ID[x]) for x in full_order) / len(full_order))
    impact = round(sum(local_impact_score(DEST_BY_ID[x]) for x in full_order) / len(full_order))

    return dict(
        stops=stops, total_distance_km=round(total_km, 1), total_duration_min=total_min,
        estimated_cost=round(total_cost), readiness=readiness, local_impact=impact,
        transport_mode=transport_mode,
    )


def build_route_from_certified(cert, start_date, travelers):
    stops = []
    cur = start_date
    total_km = 0.0
    total_cost = 0.0
    prev = None
    for idx, did in enumerate(cert["stops"]):
        d = DEST_BY_ID[did]
        n = d["min_nights"]
        if prev:
            dist = haversine_km(prev["lat"], prev["lng"], d["lat"], d["lng"])
        else:
            dist = 0.0
        total_km += dist
        total_cost += d["daily_cost"] * n * travelers
        stops.append(dict(
            destination_id=did, name=d["name"], order=idx + 1, nights=n,
            check_in=cur.isoformat(), check_out=(cur + timedelta(days=n)).isoformat(),
            distance_from_prev_km=round(dist, 1), drive_min=drive_minutes(dist),
            highlights=d["highlights"], daily_cost=d["daily_cost"],
            lat=d["lat"], lng=d["lng"],
        ))
        cur = cur + timedelta(days=n)
        prev = d
    return dict(
        stops=stops, total_distance_km=round(total_km, 1),
        total_duration_min=drive_minutes(total_km), estimated_cost=round(total_cost),
        readiness=80, local_impact=cert["local_impact"],
    )


# ----------------------------- Day Scheduler -----------------------------
def _fmt(minutes):
    h = (minutes // 60) % 24
    m = minutes % 60
    return f"{h:02d}:{m:02d}"


# ----------------------------- Real hotels per city -----------------------------
# name, stars, area, approx nightly SAR, type
HOTELS = {
    "riyadh": [
        ("The Ritz-Carlton Riyadh", 5, "Diplomatic Quarter", 1400, "Luxury"),
        ("Four Seasons Hotel Riyadh", 5, "Kingdom Centre", 1500, "Luxury"),
        ("Hyatt Regency Riyadh Olaya", 5, "Olaya", 850, "Luxury"),
        ("Aloft Riyadh", 4, "Olaya", 480, "Mid-Range"),
        ("ibis Riyadh Olaya Street", 3, "Olaya", 260, "Budget"),
    ],
    "jeddah": [
        ("The Ritz-Carlton Jeddah", 5, "Corniche", 1300, "Luxury"),
        ("Park Hyatt Jeddah", 5, "Marina", 1100, "Luxury"),
        ("Radisson Blu Hotel Jeddah", 4, "Al Salamah", 520, "Mid-Range"),
        ("ibis Jeddah City Center", 3, "Al Rawdah", 250, "Budget"),
    ],
    "alula": [
        ("Habitas AlUla", 5, "Ashar Valley", 2200, "Luxury"),
        ("Banyan Tree AlUla", 5, "Ashar Valley", 2600, "Luxury"),
        ("Shaden Resort", 4, "AlUla", 900, "Mid-Range"),
        ("Sahary AlUla Resort", 3, "AlUla", 420, "Budget"),
    ],
    "abha": [
        ("Abha Palace Hotel", 5, "Al Soudah Rd", 700, "Luxury"),
        ("Blue Inn Boutique Hotel", 4, "Abha", 450, "Mid-Range"),
        ("Al Eairy Furnished Apartments", 3, "Abha", 220, "Budget"),
    ],
    "albaha": [
        ("Golden Tulip Al Baha", 4, "Al Baha", 380, "Mid-Range"),
        ("Safir Al Baha Hotel", 3, "Al Baha", 240, "Budget"),
    ],
    "taif": [
        ("InterContinental Taif", 5, "Taif", 750, "Luxury"),
        ("Velar Hotel", 4, "Taif", 420, "Mid-Range"),
        ("Boudl Taif", 3, "Taif", 230, "Budget"),
    ],
    "hail": [
        ("Golden Tulip Hail", 4, "Hail", 380, "Mid-Range"),
        ("Millennium Hail Hotel", 5, "Hail", 600, "Luxury"),
        ("Oyo Hail", 3, "Hail", 200, "Budget"),
    ],
    "qassim": [
        ("Movenpick Hotel Qassim", 5, "Buraidah", 650, "Luxury"),
        ("Golden Tulip Buraidah", 4, "Buraidah", 380, "Mid-Range"),
        ("Boudl Buraidah", 3, "Buraidah", 220, "Budget"),
    ],
    "makkah": [
        ("Fairmont Makkah Clock Royal Tower", 5, "Abraj Al Bait", 1600, "Luxury"),
        ("Swissotel Makkah", 5, "Abraj Al Bait", 1200, "Luxury"),
        ("Hilton Suites Makkah", 4, "Ibrahim Al Khalil", 700, "Mid-Range"),
    ],
    "madinah": [
        ("The Oberoi Madina", 5, "Central Area", 1400, "Luxury"),
        ("Pullman Zamzam Madina", 5, "Central Area", 900, "Luxury"),
        ("Millennium Taiba Hotel", 4, "Central Area", 550, "Mid-Range"),
    ],
    "dammam": [
        ("Sheraton Dammam Hotel", 5, "Corniche", 700, "Luxury"),
        ("Park Inn by Radisson Dammam", 4, "Al Shati", 420, "Mid-Range"),
        ("ibis Dammam", 3, "Dammam", 230, "Budget"),
    ],
    "khobar": [
        ("Le Meridien Al Khobar", 5, "Corniche", 750, "Luxury"),
        ("DoubleTree by Hilton Al Khobar", 4, "Al Rakah", 480, "Mid-Range"),
        ("Holiday Inn Al Khobar", 3, "Al Khobar", 260, "Budget"),
    ],
    "tabuk": [
        ("Grand Millennium Tabuk", 5, "Tabuk", 600, "Luxury"),
        ("Holiday Inn Tabuk", 4, "Tabuk", 380, "Mid-Range"),
        ("Oyo Tabuk", 3, "Tabuk", 200, "Budget"),
    ],
    "jazan": [
        ("Radisson Blu Resort Jazan", 5, "Corniche", 650, "Luxury"),
        ("Holiday Jazan Hotel", 4, "Jazan", 380, "Mid-Range"),
        ("Al Eairy Jazan", 3, "Jazan", 200, "Budget"),
    ],
    "najran": [
        ("Gloria Inn Najran", 4, "Najran", 350, "Mid-Range"),
        ("Hyatt Najran", 3, "Najran", 220, "Budget"),
    ],
}


# ----------------------------- Per-member budget estimation -----------------------------
# Approx SAR costs by price tier (1-3) for one visit / meal.
_PRICE_SAR = {1: 40, 2: 90, 3: 180}

def estimate_member_budget(trip, member, member_item_votes):
    """Estimate one member's trip cost from their choices.
    Returns dict with accommodation, food, activities, transport, total, per_day."""
    import data as _data
    stops = trip["route"].get("stops", [])
    nights_total = sum(s["nights"] for s in stops) or 1
    budget_tier = trip.get("budget_tier", "Mid-range")

    # Accommodation: avg nightly rate of the member's tier across stops
    nightly_rates = []
    for s in stops:
        hs = hotels_for(s["destination_id"], budget_tier)
        if hs:
            nightly_rates.append(hs[0][3])  # top pick nightly SAR
    avg_nightly = sum(nightly_rates) / len(nightly_rates) if nightly_rates else 400
    accommodation = avg_nightly * nights_total

    # Food & activities from the member's own item votes (or defaults)
    food = 0.0
    activities = 0.0
    if member_item_votes:
        for v in member_item_votes:
            # find the place to read its price tier
            price_tier = 2
            for r in _data.RESTAURANTS + _data.ATTRACTIONS:
                if r[0] == v.get("item_id") or r[2] == v.get("item_name"):
                    price_tier = r[7]
                    break
            cost = _PRICE_SAR.get(price_tier, 90)
            if v.get("item_type") == "restaurant":
                food += cost
            else:
                activities += cost
    else:
        # default: 2 meals + 2 activities per day at mid tier
        food = 2 * _PRICE_SAR[2] * nights_total
        activities = 2 * _PRICE_SAR[2] * nights_total

    # Transport: share of route distance by mode
    mode = trip["route"].get("transport_mode", "road")
    total_km = trip["route"].get("total_distance_km", 0)
    per_km = {"road": 0.5, "air": 1.2, "rail": 0.35}.get(mode, 0.5)
    transport = total_km * per_km

    total = accommodation + food + activities + transport
    return dict(
        accommodation=round(accommodation), food=round(food),
        activities=round(activities), transport=round(transport),
        total=round(total), per_day=round(total / nights_total),
        nights=nights_total, tier=budget_tier,
    )


def hotels_for(dest_id, budget_tier="mid", accommodation=None):
    """Return real hotels for a city filtered by budget tier."""
    hs = HOTELS.get(dest_id, [])
    if not hs:
        return []
    tier_map = {"Budget": "Budget", "Mid-range": "Mid-Range", "Luxury": "Luxury"}
    want = tier_map.get(budget_tier, "Mid-Range")
    # prefer matching tier, else return all sorted by stars
    matched = [h for h in hs if h[4] == want]
    rest = [h for h in hs if h[4] != want]
    ordered = matched + sorted(rest, key=lambda x: -x[1])
    return ordered


def schedule_trip_days(dest_id, nights, day_start, day_end, pace, cuisine_ids):
    """Generate a schedule for EACH day of the stay (not just one day)."""
    days = max(1, int(nights))
    all_days = []
    attrs = attractions_for(dest_id)
    # rotate attractions across days so each day differs
    for d in range(days):
        day_attrs = attrs[d:] + attrs[:d]  # rotate
        all_days.append(_schedule_one_day(dest_id, day_start, day_end, pace, cuisine_ids, day_attrs, d + 1))
    return all_days


def _schedule_one_day(dest_id, day_start, day_end, pace, cuisine_ids, attrs, day_num):
    """Internal: schedule a single day given a rotated attraction list."""
    start_min = int(day_start) * 60
    end_min = int(day_end) * 60
    lunch_at = 13 * 60
    dinner_at = 19 * 60 + 30
    gap = 30

    rests = restaurants_by_cuisines(dest_id, cuisine_ids)
    lunch = rests[(day_num - 1) % len(rests)] if rests else None
    dinner = rests[day_num % len(rests)] if rests else None

    target = 5 if pace == "action_packed" else (3 if pace == "relaxed" else 4)
    items = []
    for a in attrs[:target]:
        kind = "heavy" if a[3] == "Nature" else ("light" if a[3] == "Religious" else "medium")
        items.append(dict(label=a[2], kind=kind, rating=a[6], dur=a[8]))
    order_map = {"light": 0, "medium": 1, "heavy": 2}
    items.sort(key=lambda x: order_map[x["kind"]])

    out = []
    cursor = start_min
    lunch_added = False
    dinner_added = False

    def add_meal(label, place):
        nonlocal cursor
        dur = place[8] if place else 60
        name = f"{label} — {place[2]}" if place else label
        out.append(dict(time=_fmt(cursor), end=_fmt(cursor + dur), label=name,
                        kind="meal", rating=(place[6] if place else None)))
        cursor += dur + gap

    for it in items:
        dur = it["dur"]
        if pace == "relaxed":
            dur = int(dur * 1.15)
        elif pace == "action_packed":
            dur = int(dur * 0.85)
        if not lunch_added and lunch_at - 30 <= cursor <= lunch_at + 60:
            lunch_added = True
            add_meal("Lunch", lunch)
        if cursor + dur > end_min:
            break
        out.append(dict(time=_fmt(cursor), end=_fmt(cursor + dur), label=it["label"],
                        kind="activity", rating=it["rating"]))
        cursor += dur + gap
        if not lunch_added and cursor >= lunch_at:
            lunch_added = True
            add_meal("Lunch", lunch)
        if not dinner_added and dinner_at - 30 <= cursor <= dinner_at + 60:
            dinner_added = True
            add_meal("Dinner", dinner)
    return out


def schedule_day(dest_id, day_start, day_end, pace, cuisine_ids):
    """Distribute a day's activities across the tourist's waking hours with real
    attractions and cuisine-matched restaurants."""
    start_min = day_start * 60
    end_min = day_end * 60
    lunch_at = 13 * 60
    dinner_at = 19 * 60 + 30
    gap = 30

    attrs = attractions_for(dest_id)
    rests = restaurants_by_cuisines(dest_id, cuisine_ids)
    lunch = rests[0] if rests else None
    dinner = rests[1] if len(rests) > 1 else (rests[0] if rests else None)

    target = 5 if pace == "action_packed" else (3 if pace == "relaxed" else 4)
    items = []
    for a in attrs[:target]:
        kind = "heavy" if a[3] == "Nature" else ("light" if a[3] == "Religious" else "medium")
        items.append(dict(label=a[2], kind=kind, rating=a[6], dur=a[8]))
    order_map = {"light": 0, "medium": 1, "heavy": 2}
    items.sort(key=lambda x: order_map[x["kind"]])

    out = []
    cursor = start_min
    lunch_added = False
    dinner_added = False

    def add_meal(label, place):
        nonlocal cursor
        dur = place[8] if place else 60
        name = f"{label} — {place[2]}" if place else label
        out.append(dict(time=_fmt(cursor), end=_fmt(cursor + dur), label=name,
                        kind="meal", rating=(place[6] if place else None)))
        cursor += dur + gap

    for it in items:
        dur = it["dur"]
        if pace == "relaxed":
            dur = int(dur * 1.15)
        elif pace == "action_packed":
            dur = int(dur * 0.85)
        if not lunch_added and lunch_at - 30 <= cursor <= lunch_at + 60:
            lunch_added = True
            add_meal("Lunch", lunch)
        if cursor + dur > end_min:
            break
        out.append(dict(time=_fmt(cursor), end=_fmt(cursor + dur), label=it["label"],
                        kind="activity", rating=it["rating"]))
        cursor += dur + gap
        if not lunch_added and cursor >= lunch_at:
            lunch_added = True
            add_meal("Lunch", lunch)
        if not dinner_added and dinner_at - 30 <= cursor <= dinner_at + 60:
            dinner_added = True
            add_meal("Dinner", dinner)
    return out


# ----------------------------- Invite codes -----------------------------
CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def generate_invite_code():
    return "TRP-" + "".join(random.choice(CODE_ALPHABET) for _ in range(5))


def normalize_invite_code(code):
    return (code or "").strip().upper()


def is_valid_invite_code(code):
    c = normalize_invite_code(code)
    if not c.startswith("TRP-") or len(c) != 9:
        return False
    return all(ch in CODE_ALPHABET for ch in c[4:])


# ----------------------------- Consensus -----------------------------
def destination_consensus(votes):
    """votes: list of dicts {destination_id, score(1-5)}. Return avg per destination."""
    agg = {}
    for v in votes:
        agg.setdefault(v["destination_id"], []).append(v["score"])
    return {k: round(sum(vs) / len(vs), 2) for k, vs in agg.items()}


def route_consensus(member_interests):
    """Average interest vectors across members -> consensus score 0-100."""
    if not member_interests:
        return 0
    keys = member_interests[0].keys()
    avg = {k: sum(m.get(k, 0) for m in member_interests) / len(member_interests) for k in keys}
    return round((sum(avg.values()) / (len(keys) * 5)) * 100)


def rank_by_consensus(votes):
    cons = destination_consensus(votes)
    return sorted(cons.items(), key=lambda x: -x[1])


def rank_items_by_consensus(item_votes, destination_id=None, item_type=None):
    """Average score per item (attraction/restaurant), optionally filtered by
    destination and/or type. Returns list of (item_name, avg, count) sorted desc."""
    agg = {}
    for v in item_votes:
        if destination_id and v.get("destination_id") != destination_id:
            continue
        if item_type and v.get("item_type") != item_type:
            continue
        key = (v.get("item_type"), v.get("item_name"))
        agg.setdefault(key, []).append(v.get("score", 0))
    out = []
    for (itype, name), scores in agg.items():
        avg = round(sum(scores) / len(scores), 1) if scores else 0
        out.append((name, avg, len(scores), itype))
    out.sort(key=lambda x: -x[1])
    return out


# ----------------------------- Personalized recommendations -----------------------------
def aggregate_preferences(past_interests):
    """Average interest vectors across a user's past trips -> taste profile."""
    if not past_interests:
        return {}
    keys = past_interests[0].keys()
    return {k: round(sum(p.get(k, 0) for p in past_interests) / len(past_interests), 2) for k in keys}


def recommend_destinations(taste_profile, visited_ids=None, include_holy=False, limit=5,
                           user_ratings=None):
    """Recommend destinations matching the user's taste profile, excluding visited ones.
    user_ratings: {destination_id: stars 1-5} — boosts liked (>=4) and dampens disliked (<=2).
    Returns list of (destination, match_score 0-100, reason)."""
    visited_ids = set(visited_ids or [])
    user_ratings = user_ratings or {}
    if not taste_profile:
        return []
    # dominant interests (top 2)
    top = sorted(taste_profile.items(), key=lambda x: -x[1])[:2]
    top_keys = [k for k, _ in top]
    recs = []
    for d in DEST_BY_ID.values():
        if d["id"] in visited_ids:
            continue
        if d["holy"] and not include_holy:
            continue
        score = destination_score(d, taste_profile)
        # feedback loop: adjust by the user's own past rating of this destination
        stars = user_ratings.get(d["id"])
        if stars is not None:
            if stars >= 4:
                score = min(1.0, score * 1.15)   # boost liked
            elif stars <= 2:
                score = score * 0.6              # dampen disliked
        match = round(score * 100)
        # reason from dominant matching interest
        best_k = max(top_keys, key=lambda k: d["interests"].get(k, 0)) if top_keys else None
        reason = ""
        if best_k:
            from data import INTEREST_LABELS
            reason = f"Strong in {INTEREST_LABELS.get(best_k, best_k)}"
        if stars is not None:
            reason += f" · You rated it {stars}★"
        recs.append((d, match, reason))
    recs.sort(key=lambda x: -x[1])
    return recs[:limit]
