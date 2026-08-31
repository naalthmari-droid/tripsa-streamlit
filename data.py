"""TRIPSA — Real data layer: destinations, restaurants, attractions, certified routes."""

# ----------------------------- Destinations -----------------------------
# Each: id, name, region, lat, lng, interests(0-5), daily_cost, occupancy, season, holy, min_nights, highlights, blurb
DESTINATIONS = [
    dict(id="riyadh", name="Riyadh", region="Riyadh Province", lat=24.7136, lng=46.6753,
         interests=dict(history_culture=4, nature_adventure=2, entertainment=5, shopping_luxury=5, relaxation=3, religious=1),
         daily_cost=550, occupancy=56, season="winter", holy=False, min_nights=2,
         highlights=["At-Turaif, Diriyah", "Riyadh Season", "National Museum", "Kingdom Tower"],
         blurb="The pulsing capital — world-class entertainment, luxury shopping and Diriyah heritage."),
    dict(id="diriyah", name="Diriyah", region="Riyadh Province", lat=24.7325, lng=46.5747,
         interests=dict(history_culture=5, nature_adventure=1, entertainment=3, shopping_luxury=4, relaxation=3, religious=1),
         daily_cost=480, occupancy=56, season="winter", holy=False, min_nights=1,
         highlights=["At-Turaif (UNESCO)", "Bujairi Terrace", "Diriyah Season"],
         blurb="Birthplace of the Saudi state — UNESCO heritage and elegant evenings."),
    dict(id="jeddah", name="Jeddah", region="Makkah Province", lat=21.4858, lng=39.1925,
         interests=dict(history_culture=4, nature_adventure=3, entertainment=4, shopping_luxury=4, relaxation=4, religious=2),
         daily_cost=500, occupancy=59, season="winter", holy=False, min_nights=2,
         highlights=["Historic Jeddah (Al-Balad)", "Corniche", "King Fahd Fountain", "Diving"],
         blurb="Bride of the Red Sea — maritime heritage and a vibrant waterfront."),
    dict(id="makkah", name="Makkah", region="Makkah Province", lat=21.3891, lng=39.8579,
         interests=dict(history_culture=3, nature_adventure=1, entertainment=1, shopping_luxury=2, relaxation=2, religious=5),
         daily_cost=450, occupancy=60, season="all_year", holy=True, min_nights=2,
         highlights=["Masjid al-Haram", "Jabal al-Nour", "Two Holy Mosques Museum"],
         blurb="The holiest city — a spiritual destination for Muslims."),
    dict(id="madinah", name="Madinah", region="Madinah Province", lat=24.5247, lng=39.5692,
         interests=dict(history_culture=4, nature_adventure=1, entertainment=1, shopping_luxury=2, relaxation=3, religious=5),
         daily_cost=420, occupancy=82, season="all_year", holy=True, min_nights=2,
         highlights=["Prophet's Mosque", "Mount Uhud", "Quba Mosque"],
         blurb="The radiant city — serenity and rich Islamic history."),
    dict(id="alula", name="AlUla", region="Madinah Province", lat=26.6085, lng=37.9232,
         interests=dict(history_culture=5, nature_adventure=5, entertainment=3, shopping_luxury=3, relaxation=4, religious=1),
         daily_cost=700, occupancy=77, season="winter", holy=False, min_nights=2,
         highlights=["Hegra (Madain Salih)", "Elephant Rock", "Heritage Oasis Trail", "Maraya"],
         blurb="An open-air museum — ancient civilizations, stunning desert and luxury experiences."),
    dict(id="abha", name="Abha", region="Aseer Province", lat=18.2465, lng=42.5117,
         interests=dict(history_culture=3, nature_adventure=5, entertainment=3, shopping_luxury=2, relaxation=4, religious=1),
         daily_cost=380, occupancy=55, season="summer", holy=False, min_nights=2,
         highlights=["Jabal Soudah", "Rijal Almaa Village", "Abha Cable Car", "Clouds"],
         blurb="The Kingdom's summer resort — green mountains and cool summer air."),
    dict(id="taif", name="Taif", region="Makkah Province", lat=21.2703, lng=40.4158,
         interests=dict(history_culture=3, nature_adventure=4, entertainment=3, shopping_luxury=2, relaxation=4, religious=2),
         daily_cost=350, occupancy=52, season="summer", holy=False, min_nights=1,
         highlights=["Rose Farms", "Al-Hada Mountain", "Souk Okaz", "Al-Hada Cable Car"],
         blurb="City of roses — a historic summer resort with natural fragrances."),
    dict(id="hail", name="Hail", region="Hail Province", lat=27.5114, lng=41.7208,
         interests=dict(history_culture=4, nature_adventure=4, entertainment=2, shopping_luxury=1, relaxation=3, religious=1),
         daily_cost=300, occupancy=48, season="winter", holy=False, min_nights=1,
         highlights=["Jubbah Rock Art (UNESCO)", "Aja Mountains", "Hatim Al-Tai House", "Al-Daidahan Reserve"],
         blurb="Gateway to the north — UNESCO inscriptions and Hatimi generosity."),
    dict(id="qassim", name="Qassim (Buraydah/Unaizah)", region="Qassim Province", lat=26.3260, lng=43.9750,
         interests=dict(history_culture=4, nature_adventure=2, entertainment=2, shopping_luxury=2, relaxation=3, religious=1),
         daily_cost=280, occupancy=50, season="winter", holy=False, min_nights=1,
         highlights=["Bassam House", "Al-Musawkaf Market", "Date Season", "Al-Oqilat Museum"],
         blurb="The agricultural heart of Najd — authentic heritage and world-class dates."),
    dict(id="alahsa", name="Al-Ahsa", region="Eastern Province", lat=25.3833, lng=49.5833,
         interests=dict(history_culture=4, nature_adventure=3, entertainment=2, shopping_luxury=2, relaxation=4, religious=1),
         daily_cost=320, occupancy=50, season="winter", holy=False, min_nights=1,
         highlights=["Al-Ahsa Oasis (UNESCO)", "Jabal Qara", "Qaisariah Souq", "Yellow Lake"],
         blurb="The world's largest oasis — palms, springs and history."),
    dict(id="dammam_khobar", name="Dammam & Khobar", region="Eastern Province", lat=26.4207, lng=50.0888,
         interests=dict(history_culture=2, nature_adventure=3, entertainment=4, shopping_luxury=4, relaxation=4, religious=1),
         daily_cost=450, occupancy=58, season="winter", holy=False, min_nights=1,
         highlights=["Khobar Corniche", "Coral Island", "Ithra (Dhahran)", "Half Moon Beach"],
         blurb="The Gulf waterfront — beaches, shopping and contemporary culture."),
    dict(id="tabuk", name="Tabuk", region="Tabuk Province", lat=28.3838, lng=36.5550,
         interests=dict(history_culture=3, nature_adventure=5, entertainment=2, shopping_luxury=1, relaxation=3, religious=1),
         daily_cost=320, occupancy=45, season="winter", holy=False, min_nights=1,
         highlights=["Tabuk Castle", "Wadi Disah", "NEOM Bay", "Jabal al-Lawz"],
         blurb="Gateway to the northwest — enchanting valleys and Lawz snow."),
    dict(id="yanbu", name="Yanbu", region="Madinah Province", lat=24.0896, lng=38.0618,
         interests=dict(history_culture=2, nature_adventure=4, entertainment=3, shopping_luxury=2, relaxation=5, religious=1),
         daily_cost=400, occupancy=50, season="winter", holy=False, min_nights=1,
         highlights=["Yanbu Coral Reefs", "Old Town", "Diving", "The Lake"],
         blurb="Pearl of the Red Sea — diving and calm beaches."),
    dict(id="albaha", name="Al-Baha", region="Al-Baha Province", lat=20.0129, lng=41.4677,
         interests=dict(history_culture=3, nature_adventure=5, entertainment=2, shopping_luxury=1, relaxation=4, religious=1),
         daily_cost=300, occupancy=46, season="summer", holy=False, min_nights=1,
         highlights=["Dhee Ayn Village", "Raghadan Forest", "Qamrah Mountains", "Hiking Trails"],
         blurb="Garden of the Hejaz — misty forests and hanging villages."),
]

DEST_BY_ID = {d["id"]: d for d in DESTINATIONS}
HOLY_IDS = [d["id"] for d in DESTINATIONS if d["holy"]]

INTEREST_LABELS = {
    "history_culture": "History & Culture",
    "nature_adventure": "Nature & Adventure",
    "entertainment": "Entertainment",
    "shopping_luxury": "Shopping & Luxury",
    "relaxation": "Relaxation & Wellness",
    "religious": "Religious Tourism",
}

# ----------------------------- Cuisines -----------------------------
CUISINES = [
    ("traditional_saudi", "Traditional Saudi"),
    ("middle_eastern", "Middle Eastern"),
    ("asian", "Asian"),
    ("european", "European"),
    ("international_fusion", "International / Fusion"),
    ("fast_food", "Fast Food"),
]
CUISINE_LABELS = dict(CUISINES)

ACCOMMODATION_TYPES = [
    "Budget (hostel / 1-2★)", "Mid-range (3-4★ hotel)", "Luxury (5★ hotel)",
    "Resort", "Desert camp / Glamping", "Serviced apartment",
]

# ----------------------------- Restaurants -----------------------------
# id, dest, name, cuisine, lat, lng, rating, price(1-3), duration_min
RESTAURANTS = [
    ("najd_village", "riyadh", "Najd Village", "traditional_saudi", 24.7136, 46.6900, 4.5, 2, 90),
    ("takya", "riyadh", "Takya", "traditional_saudi", 24.7200, 46.6600, 4.4, 2, 80),
    ("suhail", "riyadh", "Suhail", "middle_eastern", 24.7300, 46.6700, 4.6, 3, 100),
    ("nobu_riyadh", "riyadh", "Nobu", "asian", 24.7117, 46.6744, 4.7, 3, 110),
    ("lusin", "riyadh", "Lusin", "european", 24.7400, 46.6500, 4.5, 3, 100),
    ("section_b", "riyadh", "Section B", "fast_food", 24.7050, 46.6800, 4.3, 1, 50),
    ("bujairi_terrace", "diriyah", "Bujairi Terrace", "international_fusion", 24.7330, 46.5750, 4.6, 3, 100),
    ("tatel_diriyah", "diriyah", "Tatel", "european", 24.7335, 46.5755, 4.5, 3, 100),
    ("albaik", "jeddah", "Al Baik", "fast_food", 21.4900, 39.1800, 4.5, 1, 40),
    ("twina", "jeddah", "Twina", "middle_eastern", 21.5500, 39.1500, 4.6, 2, 90),
    ("shababik", "jeddah", "Shababik", "middle_eastern", 21.5600, 39.1400, 4.4, 2, 85),
    ("toki", "jeddah", "Toki", "asian", 21.5700, 39.1300, 4.5, 3, 100),
    ("il_gabbiano", "jeddah", "Il Gabbiano", "european", 21.5800, 39.1200, 4.6, 3, 110),
    ("albaik_makkah", "makkah", "Al Baik (Aziziyah)", "fast_food", 21.3900, 39.8500, 4.4, 1, 40),
    ("al_tazaj", "makkah", "Al Tazaj", "middle_eastern", 21.4000, 39.8600, 4.2, 1, 50),
    ("arabesque", "madinah", "Arabesque", "middle_eastern", 24.4700, 39.6100, 4.4, 2, 80),
    ("albaik_madinah", "madinah", "Al Baik (Quba)", "fast_food", 24.4400, 39.6200, 4.3, 1, 40),
    ("somewhere_alula", "alula", "Somewhere", "international_fusion", 26.6100, 37.9200, 4.6, 3, 100),
    ("maraya_social", "alula", "Maraya Social", "european", 26.6200, 37.9300, 4.7, 3, 110),
    ("oasis_trail_cafe", "alula", "Oasis Cafe", "traditional_saudi", 26.6050, 37.9250, 4.3, 2, 60),
    ("al_shaya_majlis", "abha", "Al Shaya Majlis", "traditional_saudi", 18.2500, 42.5100, 4.4, 2, 90),
    ("assalam_palace", "abha", "Assalam Palace", "middle_eastern", 18.2400, 42.5200, 4.2, 2, 80),
    ("albaik_taif", "taif", "Al Baik (Shihar)", "fast_food", 21.2700, 40.4100, 4.3, 1, 40),
    ("rose_cafe_taif", "taif", "Rose Cafe", "international_fusion", 21.2800, 40.4200, 4.2, 2, 60),
    ("hail_traditional", "hail", "Hail Heritage", "traditional_saudi", 27.5100, 41.7200, 4.3, 2, 85),
    ("qassim_dates", "qassim", "Dates & Heritage", "traditional_saudi", 26.3300, 43.9700, 4.4, 2, 80),
    ("alahsa_oasis_rest", "alahsa", "Oasis Restaurant", "traditional_saudi", 25.3800, 49.5800, 4.3, 2, 85),
    ("shrimp_house", "dammam_khobar", "Shrimp House", "middle_eastern", 26.4300, 50.0900, 4.4, 2, 90),
    ("paul_khobar", "dammam_khobar", "Paul", "european", 26.4400, 50.1000, 4.5, 2, 80),
    ("tabuk_grill", "tabuk", "Tabuk Grill", "middle_eastern", 28.3800, 36.5500, 4.2, 2, 80),
    ("yanbu_seafood", "yanbu", "Yanbu Seafood", "middle_eastern", 24.0900, 38.0600, 4.5, 2, 90),
    ("albaha_mountain", "albaha", "Mountain Restaurant", "traditional_saudi", 20.0100, 41.4600, 4.2, 2, 80),
]

# ----------------------------- Attractions -----------------------------
# id, dest, name, category, lat, lng, rating, price(1-3), duration_min
ATTRACTIONS = [
    ("atturaif", "diriyah", "At-Turaif", "Heritage", 24.7325, 46.5747, 4.8, 2, 150),
    ("national_museum", "riyadh", "National Museum", "Museum", 24.6470, 46.7100, 4.6, 1, 150),
    ("kingdom_tower", "riyadh", "Kingdom Tower", "Landmark", 24.7117, 46.6744, 4.5, 2, 90),
    ("edge_of_world", "riyadh", "Edge of the World", "Nature", 24.9500, 45.9800, 4.8, 1, 240),
    ("albalad", "jeddah", "Al-Balad (Historic Jeddah)", "Heritage", 21.4858, 39.1925, 4.7, 1, 180),
    ("jeddah_corniche", "jeddah", "Jeddah Corniche", "Nature", 21.5500, 39.1100, 4.5, 1, 120),
    ("fakieh_aquarium", "jeddah", "Fakieh Aquarium", "Entertainment", 21.5600, 39.1000, 4.4, 2, 150),
    ("masjid_haram", "makkah", "Masjid al-Haram", "Religious", 21.4225, 39.8262, 5.0, 1, 180),
    ("jabal_nour", "makkah", "Jabal al-Nour", "Religious", 21.4580, 39.8780, 4.7, 1, 180),
    ("masjid_nabawi", "madinah", "Al-Masjid an-Nabawi", "Religious", 24.4672, 39.6111, 5.0, 1, 180),
    ("mount_uhud", "madinah", "Mount Uhud", "Religious", 24.5100, 39.6100, 4.8, 1, 120),
    ("quba_mosque", "madinah", "Quba Mosque", "Religious", 24.4390, 39.6170, 4.9, 1, 90),
    ("hegra", "alula", "Hegra (Madain Salih)", "Heritage", 26.7900, 37.9600, 4.9, 2, 240),
    ("elephant_rock", "alula", "Elephant Rock", "Nature", 26.6300, 37.9100, 4.7, 1, 120),
    ("maraya", "alula", "Maraya", "Landmark", 26.6200, 37.9300, 4.6, 2, 90),
    ("soudah", "abha", "Jabal Soudah", "Nature", 18.2700, 42.3700, 4.7, 1, 240),
    ("rijal_almaa", "abha", "Rijal Almaa Village", "Heritage", 18.2100, 42.2800, 4.6, 1, 180),
    ("taif_rose", "taif", "Taif Rose Farms", "Nature", 21.2900, 40.4300, 4.5, 1, 120),
    ("jubbah", "hail", "Jubbah Rock Art", "Heritage", 28.0100, 40.9100, 4.7, 1, 180),
    ("bassam_house", "qassim", "Bassam House", "Heritage", 26.3300, 43.9700, 4.4, 1, 120),
    ("alahsa_oasis", "alahsa", "Al-Ahsa Oasis", "Nature", 25.3833, 49.5833, 4.6, 1, 180),
    ("qara_mountain", "alahsa", "Jabal Qara", "Nature", 25.4100, 49.6900, 4.5, 1, 150),
    ("ithra", "dammam_khobar", "Ithra", "Museum", 26.3000, 50.1000, 4.7, 2, 180),
    ("khobar_corniche", "dammam_khobar", "Khobar Corniche", "Nature", 26.2800, 50.2200, 4.4, 1, 120),
    ("wadi_disah", "tabuk", "Wadi Disah", "Nature", 27.6300, 36.5400, 4.8, 1, 240),
    ("yanbu_lake", "yanbu", "Yanbu Lake", "Nature", 24.0900, 38.0600, 4.4, 1, 120),
    ("dhee_ayn", "albaha", "Dhee Ayn Village", "Heritage", 19.9300, 41.4400, 4.6, 1, 180),
]

def restaurants_for(dest_id):
    rows = [r for r in RESTAURANTS if r[1] == dest_id]
    return sorted(rows, key=lambda r: -r[6])

def attractions_for(dest_id):
    rows = [a for a in ATTRACTIONS if a[1] == dest_id]
    return sorted(rows, key=lambda a: -a[6])

def restaurants_by_cuisines(dest_id, cuisine_ids):
    allr = restaurants_for(dest_id)
    if not cuisine_ids:
        return allr
    matched = [r for r in allr if r[3] in cuisine_ids]
    return matched if matched else allr

# ----------------------------- Railway lines (real, SAR) -----------------------------
RAIL_LINES = [
    dict(id="haramain", name="Haramain High-Speed Railway", operator="SAR",
         stops=["makkah", "jeddah", "madinah"], note="Makkah - Jeddah - Madinah (up to 300 km/h)"),
    dict(id="riyadh_dammam", name="Riyadh-Dammam Railway", operator="SAR",
         stops=["riyadh", "dammam", "khobar"], note="Riyadh - Dammam / Al-Khobar"),
    dict(id="north", name="North-South Railway", operator="SAR",
         stops=["riyadh", "qassim", "hail"], note="Riyadh - Qassim - Hail"),
]

def rail_between(a_id, b_id):
    """Return the rail line dict connecting two destinations, or None."""
    for line in RAIL_LINES:
        if a_id in line["stops"] and b_id in line["stops"]:
            return line
    return None

def rail_options_for_route(dest_ids):
    """Return list of (from_id, to_id, line) for consecutive stops connected by rail."""
    out = []
    for i in range(len(dest_ids) - 1):
        line = rail_between(dest_ids[i], dest_ids[i + 1])
        if line:
            out.append((dest_ids[i], dest_ids[i + 1], line))
    return out


# ----------------------------- Airports (IATA) -----------------------------
AIRPORTS = {
    "riyadh": "RUH", "diriyah": "RUH", "jeddah": "JED", "makkah": "JED",
    "madinah": "MED", "alula": "ULH", "abha": "AHB", "taif": "TIF",
    "hail": "HAS", "qassim": "ELQ", "alahsa": "HOF", "dammam": "DMM",
    "khobar": "DMM", "dammam_khobar": "DMM", "tabuk": "TUU", "yanbu": "YNB",
    "albaha": "ABT", "jazan": "GIZ", "najran": "EAM",
}

def airport_for(dest_id):
    return AIRPORTS.get(dest_id)

def transport_options(a_id, b_id, km, engine):
    """Build a comparison of transport options for one leg (road/air/rail)."""
    opts = []
    for mode in ("road", "air", "rail"):
        m = engine.TRANSPORT_MODES[mode]
        mins = engine.travel_minutes(km, mode)
        avail, note = True, ""
        if mode == "air":
            fa, ta = airport_for(a_id), airport_for(b_id)
            if fa and ta:
                note = f"{fa} → {ta} · ~{max(1, round(mins/60))}h incl. airport time"
            else:
                avail, note = False, "No direct airport on this leg"
        elif mode == "rail":
            line = rail_between(a_id, b_id)
            if line:
                note = f"{line['name']} · {line['note']}"
            else:
                avail, note = False, "No rail line connects these cities"
        else:
            note = f"{round(km)} km drive"
        opts.append(dict(mode=mode, icon=m["icon"], label=m["label"], minutes=mins,
                         available=avail, note=note))
    return opts


# ----------------------------- Certified Routes -----------------------------
CERTIFIED_ROUTES = [
    dict(
        id="north_route", name="The Northern Route", authority="Saudi Tourism Authority",
        days=5, distance_km=630, local_impact=78,
        stops=["riyadh", "qassim", "hail"],
        description="A heritage corridor linking Riyadh, Qassim and Hail — UNESCO rock art, mud-brick towns and Najdi culture.",
        highlights=["At-Turaif", "Bassam House", "Jubbah Rock Art"],
    ),
    dict(
        id="oasis_trail", name="Heritage Oasis Trail", authority="Royal Commission for AlUla",
        days=3, distance_km=45, local_impact=85,
        stops=["alula"],
        description="A walking trail through AlUla's ancient oasis — farms, mud-brick villages and heritage sites.",
        highlights=["Hegra", "Elephant Rock", "Old Town"],
    ),
]
