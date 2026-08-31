"""TRIPSA — Saudi Route Intelligence. Streamlit app (English)."""
import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime, date
import json, os
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

import data
import engine
import db
from style import CUSTOM_CSS, LOTTIE

st.set_page_config(page_title="TRIPSA — Saudi Route Intelligence", page_icon="🧭", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
db.init_db()

@st.cache_data
def load_lottie(path):
    """Load a Lottie animation from a LOCAL file (instant, no network)."""
    try:
        with open(os.path.join(os.path.dirname(__file__), path)) as f:
            return json.load(f)
    except Exception:
        return None

# ---------------- session state ----------------
for k, v in dict(page="home", trip_id=None, member_id=None, member_name="").items():
    if k not in st.session_state:
        st.session_state[k] = v


def go(page, **kw):
    st.session_state.page = page
    for kk, vv in kw.items():
        st.session_state[kk] = vv
    # keep the top nav in sync with programmatic navigation
    _labels = {"home":"Home","create":"Create","join":"Join","routes":"Routes"}
    if page in _labels:
        st.session_state._nav = _labels[page]
    st.rerun()


def hero():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("""
        <div class="hero">
          <div class="brand"><span class="dot"></span> TRIPSA</div>
          <h1>Plan your Saudi road trip<br/>with intelligence.</h1>
          <p>TRIPSA builds an optimized route between cities — with distance, stay dates,
          cost and readiness — and lets your group vote & reach consensus via a single invite code.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        anim = load_lottie(LOTTIE["travel"])
        if anim:
            st_lottie(anim, height=220, key="hero")


def fmt_drive(m):
    if m < 60:
        return f"{m}m"
    h, mm = divmod(m, 60)
    return f"{h}h {mm}m" if mm else f"{h}h"


def fmt_date(iso):
    return datetime.fromisoformat(iso).strftime("%b %d")


# ============================================================ HOME
def page_home():
    hero()
    st.markdown("<br/>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><h3>🧭 Optimized Routes</h3><div class="sub">A TSP engine orders your cities to minimize drive time, with per-stop stay dates.</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><h3>🤝 Group Consensus</h3><div class="sub">Invite code, member preferences, voting and a live group-consensus score.</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><h3>📊 Readiness & Impact</h3><div class="sub">Readiness (0-100) and local economic impact for every route.</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec">Get started</div>', unsafe_allow_html=True)
    a, b, c = st.columns([1, 1, 1])
    if a.button("✨ Create a trip", use_container_width=True):
        go("create")
    if b.button("🔑 Join with code", use_container_width=True):
        go("join")
    if c.button("🗺️ Certified routes", use_container_width=True):
        go("routes")

    trips = db.list_trips()
    if trips:
        st.markdown('<div class="sec">Recent trips</div>', unsafe_allow_html=True)
        st.markdown('<div class="stagger">', unsafe_allow_html=True)
        for t in trips[:6]:
            if st.button(f"📍 {t['title']} — {t['invite_code']}", key=f"t{t['id']}", use_container_width=True):
                go("detail", trip_id=t["id"])
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================ CREATE
def page_create():
    st.markdown('<div class="sec">✨ Create your trip</div>', unsafe_allow_html=True)
    with st.form("create"):
        c1, c2 = st.columns(2)
        title = c1.text_input("Trip title", "Northern Adventure")
        owner = c2.text_input("Your name", "Sara")
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("Your age", 18, 90, 28)
        travelers = c2.number_input("Travelers", 1, 20, 2)
        budget = c3.selectbox("Budget tier", ["Budget", "Mid-range", "Luxury"])

        route_mode = st.radio("How to build your route?", ["Pick cities myself", "Use a certified route"], horizontal=True)
        certified_id = None
        if route_mode == "Pick cities myself":
            start = st.selectbox("Starting point", [d["id"] for d in data.DESTINATIONS],
                                 format_func=lambda x: data.DEST_BY_ID[x]["name"])
            others = [d["id"] for d in data.DESTINATIONS if d["id"] != start]
            chosen = st.multiselect("Cities to visit (empty = smart recommendation)", others,
                                    format_func=lambda x: data.DEST_BY_ID[x]["name"])
        else:
            cert = st.selectbox("Certified route", data.CERTIFIED_ROUTES, format_func=lambda r: r["name"])
            certified_id = cert["id"]
            start = cert["stops"][0]
            chosen = []

        c1, c2 = st.columns(2)
        sd = c1.date_input("Check-in date", date(2026, 12, 1))
        ed = c2.date_input("Check-out date", date(2026, 12, 8))

        st.markdown("**Your day rhythm**")
        c1, c2 = st.columns(2)
        day_start = c1.slider("I wake up around", 5, 12, 9)
        day_end = c2.slider("I sleep around", 18, 24, 22)

        cuisines = st.multiselect("Favorite cuisines", [c[0] for c in data.CUISINES],
                                  format_func=lambda x: data.CUISINE_LABELS[x],
                                  default=["traditional_saudi"])
        accommodation = st.selectbox("Preferred accommodation", data.ACCOMMODATION_TYPES)
        pace = st.select_slider("Travel pace", ["relaxed", "moderate", "action_packed"], "moderate")

        st.markdown("**Interests (1–5)**")
        interests = {}
        cols = st.columns(3)
        for i, (k, label) in enumerate(data.INTEREST_LABELS.items()):
            interests[k] = cols[i % 3].slider(label, 1, 5, 3)
        c1, c2 = st.columns(2)
        is_group = c1.checkbox("Group trip (collaborative planning)", True)
        include_holy = c2.checkbox("Include holy cities (Makkah/Madinah — Muslims only)", False)

        if st.form_submit_button("🧭 Generate optimized route", use_container_width=True):
            if ed <= sd:
                st.error("Check-out must be after check-in.")
                return
            code = engine.generate_invite_code()
            if route_mode == "Use a certified route":
                cert = next(r for r in data.CERTIFIED_ROUTES if r["id"] == certified_id)
                route = engine.build_route_from_certified(cert, datetime.combine(sd, datetime.min.time()), travelers)
            else:
                route = engine.build_optimized_route(
                    start, chosen, interests,
                    datetime.combine(sd, datetime.min.time()), datetime.combine(ed, datetime.min.time()),
                    travelers, 500, pace, include_holy)
            tid = db.create_trip(dict(
                title=title, owner_name=owner, owner_age=age, invite_code=code,
                start_destination_id=start, start_date=str(sd), end_date=str(ed),
                travelers=travelers, budget_tier=budget, pace=pace, is_group=is_group,
                include_holy=include_holy, interests=interests, audience="tourist",
                route_mode=("certified" if route_mode == "Use a certified route" else "custom"),
                certified_route_id=certified_id, cuisines=cuisines, accommodation=accommodation,
                day_start=day_start, day_end=day_end, route=route))
            db.add_member(tid, owner, age, interests)
            # set navigation state and rerun OUTSIDE the form so the detail page renders
            st.session_state.page = "detail"
            st.session_state.trip_id = tid
            st.session_state.just_created = code
            st.rerun()


# ============================================================ DETAIL
def page_detail():
    t = db.get_trip(st.session_state.trip_id)
    if not t:
        st.warning("Trip not found.")
        return
    route = t["route"]
    stops = route.get("stops", [])

    # success banner right after creation
    if st.session_state.get("just_created"):
        st.success(f"🎉 Trip created successfully! Share invite code: **{st.session_state.just_created}**")
        st.session_state.just_created = None

    st.markdown(f'<div class="sec">🧭 {t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f"**{fmt_date(t['start_date'])} → {fmt_date(t['end_date'])}** · {t['travelers']} travelers · {t['pace']}")

    st.markdown(f'<div class="invite">🔑 {t["invite_code"]}</div>', unsafe_allow_html=True)
    st.caption("Share this code so your group can join, vote and plan together.")

    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="metric"><div class="v">{route.get("total_distance_km",0):,} km</div><div class="l">Distance</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric"><div class="v">{fmt_drive(route.get("total_duration_min",0))}</div><div class="l">Drive time</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric"><div class="v">SAR {route.get("estimated_cost",0):,}</div><div class="l">Est. cost</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="metric"><div class="v">{route.get("readiness",0)}%</div><div class="l">Readiness</div></div>', unsafe_allow_html=True)

    # Map
    st.markdown('<div class="sec">🗺️ Route map</div>', unsafe_allow_html=True)
    if stops:
        st.markdown('<div class="mapwrap">', unsafe_allow_html=True)
        m = folium.Map(location=[stops[0]["lat"], stops[0]["lng"]], zoom_start=5, tiles="CartoDB positron")
        pts = []
        for s in stops:
            pts.append([s["lat"], s["lng"]])
            folium.Marker([s["lat"], s["lng"]],
                          popup=f"<b>{s['order']}. {s['name']}</b><br>{s['nights']} nights",
                          tooltip=f"{s['order']}. {s['name']}",
                          icon=folium.Icon(color="green", icon="map-marker")).add_to(m)
        if len(pts) > 1:
            folium.PolyLine(pts, color="#2f5233", weight=3, opacity=0.8).add_to(m)
        m.fit_bounds(pts)
        st_folium(m, width=None, height=420)
        st.markdown('</div>', unsafe_allow_html=True)

    # Stops timeline
    st.markdown('<div class="sec">📍 Optimized route — stop by stop</div>', unsafe_allow_html=True)
    st.caption(f"Your day: {t['day_start']}:00 – {t['day_end']}:00 · {t.get('accommodation','')}")
    for s in stops:
        with st.container():
            st.markdown(f"""
            <div class="stop">
              <div class="num">{s['order']}</div>
              <div class="body">
                <h4>{s['name']}</h4>
                <div class="sub">🛏️ {s['nights']} night(s) · {fmt_date(s['check_in'])} → {fmt_date(s['check_out'])}
                {f"· 🚗 {s['distance_from_prev_km']} km · {fmt_drive(s['drive_min'])}" if s['order']>1 else ""}</div>
                <div>{"".join(f'<span class="tag">{h}</span>' for h in s['highlights'])}</div>
              </div>
            </div>""", unsafe_allow_html=True)
            with st.expander(f"🕒 Day schedule for {s['name']} (your hours)"):
                acts = engine.schedule_day(s["destination_id"], t["day_start"], t["day_end"], t["pace"], t["cuisines"])
                for a in acts:
                    star = f'<span class="star">★{a["rating"]}</span>' if a.get("rating") else ""
                    cls = "act meal" if a["kind"] == "meal" else "act"
                    st.markdown(f'<div class="{cls}"><span class="t">{a["time"]}–{a["end"]}</span><span class="dotm"></span><span>{a["label"]}</span>{star}</div>', unsafe_allow_html=True)

    # Members
    members = db.get_members(t["id"])
    st.markdown(f'<div class="sec">👥 Members ({len(members)})</div>', unsafe_allow_html=True)
    st.markdown('<div class="stagger">', unsafe_allow_html=True)
    for m in members:
        st.markdown(f'<span class="tag">👤 {m["name"]} · {m.get("age","—")}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if t["is_group"]:
        if st.button("🤝 Open planning room", use_container_width=True):
            go("room", trip_id=t["id"])


# ============================================================ JOIN
def page_join():
    st.markdown('<div class="sec">🔑 Join a trip</div>', unsafe_allow_html=True)
    code = st.text_input("Invite code", placeholder="TRP-XXXXX").strip().upper()
    if st.button("Find trip", use_container_width=True):
        if not engine.is_valid_invite_code(code):
            st.error("Invalid code format (TRP-XXXXX).")
            return
        t = db.get_trip_by_code(code)
        if not t:
            st.error("No trip with this code.")
            return
        st.session_state.trip_id = t["id"]
        st.success(f"Found: {t['title']}")
        with st.form("join"):
            name = st.text_input("Your name")
            age = st.number_input("Your age", 18, 90, 30)
            st.markdown("**Your interests (1–5)**")
            prefs = {}
            cols = st.columns(3)
            for i, (k, label) in enumerate(data.INTEREST_LABELS.items()):
                prefs[k] = cols[i % 3].slider(label, 1, 5, 3, key=f"j{k}")
            if st.form_submit_button("Join trip", use_container_width=True):
                mid = db.add_member(t["id"], name, age, prefs)
                st.session_state.member_id = mid
                st.session_state.member_name = name
                go("room", trip_id=t["id"])


# ============================================================ ROOM
def page_room():
    t = db.get_trip(st.session_state.trip_id)
    if not t:
        st.warning("Trip not found.")
        return
    stops = t["route"].get("stops", [])
    members = db.get_members(t["id"])
    votes = db.get_votes(t["id"])

    st.markdown(f'<div class="sec">🤝 Planning room — {t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="invite">🔑 {t["invite_code"]}</div>', unsafe_allow_html=True)

    # consensus
    member_interests = [m["preferences"] for m in members if m.get("preferences")]
    cons = engine.route_consensus(member_interests)
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f'<div class="ring" style="--p:{cons}"><div class="rv">{cons}%</div></div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;color:#6b7560;font-size:13px;margin-top:6px">Group consensus</div>', unsafe_allow_html=True)
    with c2:
        anim = load_lottie(LOTTIE["group"])
        if anim:
            st_lottie(anim, height=140, key="room")

    # voting
    st.markdown('<div class="sec">🗳️ Vote on destinations</div>', unsafe_allow_html=True)
    if not st.session_state.member_id and members:
        st.session_state.member_id = members[0]["id"]
        st.session_state.member_name = members[0]["name"]
    for s in stops:
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{s['name']}**")
        score = c2.selectbox("Score", [1, 2, 3, 4, 5], index=4, key=f"v{s['destination_id']}", label_visibility="collapsed")
        if c2.button("Vote", key=f"vb{s['destination_id']}"):
            db.add_vote(t["id"], st.session_state.member_id, s["destination_id"], score)
            st.toast(f"Voted {score} for {s['name']}")
            st.rerun()

    # consensus ranking
    if votes:
        st.markdown('<div class="sec">🏆 Consensus ranking</div>', unsafe_allow_html=True)
        for did, avg in engine.rank_by_consensus(votes):
            name = data.DEST_BY_ID.get(did, {}).get("name", did)
            st.progress(min(1.0, avg / 5), text=f"{name} — {avg}/5")

    # comments
    st.markdown('<div class="sec">💬 Discussion</div>', unsafe_allow_html=True)
    with st.form("comment", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        body = c1.text_input("Share your thoughts…", label_visibility="collapsed", placeholder="Share your thoughts about the route…")
        dest = c2.selectbox("About", ["General"] + [s["destination_id"] for s in stops],
                            format_func=lambda x: "General" if x == "General" else data.DEST_BY_ID[x]["name"],
                            label_visibility="collapsed")
        if st.form_submit_button("Post", use_container_width=True) and body.strip():
            db.add_comment(t["id"], st.session_state.member_name or "Guest",
                           None if dest == "General" else dest, body.strip())
            st.rerun()
    for c in db.get_comments(t["id"]):
        dname = data.DEST_BY_ID.get(c["destination_id"], {}).get("name") if c["destination_id"] else None
        st.markdown(f'<div class="act"><span class="dotm"></span><span><b>{c["member_name"]}</b>{f" · {dname}" if dname else ""}: {c["body"]}</span></div>', unsafe_allow_html=True)


# ============================================================ ROUTES
def page_routes():
    st.markdown('<div class="sec">🗺️ Certified routes</div>', unsafe_allow_html=True)
    st.markdown('<div class="stagger">', unsafe_allow_html=True)
    for r in data.CERTIFIED_ROUTES:
        st.markdown(f"""
        <div class="card">
          <h3>{r['name']}</h3>
          <div class="sub">{r['authority']} · {r['days']} days · {r['distance_km']} km · Local impact {r['local_impact']}%</div>
          <p style="margin-top:10px">{r['description']}</p>
          <div>{"".join(f'<span class="tag">{h}</span>' for h in r['highlights'])}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================ Router
# top nav (animated option menu) — bound to session_state via key so it never
# fights with programmatic go() navigation (create/detail/room).
NAV_PAGES = ["home", "create", "join", "routes"]
NAV_LABELS = {"home":"Home", "create":"Create", "join":"Join", "routes":"Routes"}
NAV_PAGES_FROM_LABEL = {v:k for k,v in NAV_LABELS.items()}

if "_nav" not in st.session_state:
    st.session_state._nav = NAV_LABELS.get(st.session_state.page, "Home")

def _on_nav():
    lbl = st.session_state._nav
    st.session_state.page = NAV_PAGES_FROM_LABEL[lbl]

nav = option_menu(None, list(NAV_LABELS.values()),
    icons=["house", "plus-circle", "key", "map"], menu_icon="cast",
    default_index=NAV_PAGES.index(st.session_state.page) if st.session_state.page in NAV_PAGES else 0,
    orientation="horizontal", key="_nav", on_change=_on_nav,
    styles={
        "container": {"padding": "4px", "background": "#ffffff", "border-radius": "16px",
                      "border": "1px solid #ece5d2", "box-shadow": "0 8px 20px -10px rgba(28,43,33,.15)"},
        "icon": {"color": "#c9a24b", "font-size": "18px"},
        "nav-link": {"font-size": "15px", "font-weight": "600", "color": "#1c2b21",
                     "border-radius": "12px", "margin": "0 4px",
                     "--hover-color": "#f1ead6", "transition": "all .25s"},
        "nav-link-selected": {"background": "linear-gradient(135deg,#2f5233,#3e6b44)", "color": "#fff"},
    })

page = st.session_state.page
if page == "home":
    page_home()
elif page == "create":
    page_create()
elif page == "detail":
    page_detail()
elif page == "join":
    page_join()
elif page == "room":
    page_room()
elif page == "routes":
    page_routes()
