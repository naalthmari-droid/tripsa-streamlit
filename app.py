"""TRIPSA — Saudi Route Intelligence. Streamlit app (English)."""
import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime, date
import json, os
from streamlit_lottie import st_lottie

import data
import engine
import db
import notifications
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
        # elegant stat badge instead of the off-theme illustration
        st.markdown("""
        <div class="hero-badge">
          <div class="hb-num">15</div><div class="hb-lbl">Destinations</div>
          <div class="hb-div"></div>
          <div class="hb-num">2</div><div class="hb-lbl">Certified routes</div>
          <div class="hb-div"></div>
          <div class="hb-num">🤝</div><div class="hb-lbl">Group planning</div>
        </div>
        """, unsafe_allow_html=True)


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
        # Readiness & Impact is an admin/business metric — hidden from regular tourists.
        if st.session_state.get("admin_ok"):
            st.markdown('<div class="card"><h3>📊 Readiness & Impact</h3><div class="sub">Readiness (0-100) and local economic impact for every route.</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card"><h3>🍽️ Local Flavors</h3><div class="sub">Restaurant picks matched to your favorite cuisine in every city on your route.</div></div>', unsafe_allow_html=True)

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
        email = st.text_input("Your email (for trip alerts)", placeholder="you@example.com")
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
                title=title, owner_name=owner, owner_age=age, owner_email=email.strip(), invite_code=code,
                start_destination_id=start, start_date=str(sd), end_date=str(ed),
                travelers=travelers, budget_tier=budget, pace=pace, is_group=is_group,
                include_holy=include_holy, interests=interests, audience="tourist",
                route_mode=("certified" if route_mode == "Use a certified route" else "custom"),
                certified_route_id=certified_id, cuisines=cuisines, accommodation=accommodation,
                day_start=day_start, day_end=day_end, route=route))
            db.add_member(tid, owner, age, interests)
            # email confirmation (demo mode if SMTP not configured)
            ok, mode = notifications.notify_trip_created(email, owner, title, code, str(sd), str(ed))
            if email:
                st.session_state.email_note = ("📧 Confirmation email sent." if mode == "smtp"
                                               else "📧 Confirmation logged (demo mode — configure SMTP to send real emails).")
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
        if st.session_state.get("email_note"):
            st.info(st.session_state.email_note)
            st.session_state.email_note = None
        st.session_state.just_created = None

    st.markdown(f'<div class="sec">🧭 {t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f"**{fmt_date(t['start_date'])} → {fmt_date(t['end_date'])}** · {t['travelers']} travelers · {t['pace']}")

    st.markdown(f'<div class="invite">🔑 {t["invite_code"]}</div>', unsafe_allow_html=True)
    st.caption("Share this code so your group can join, vote and plan together.")

    # Readiness is an admin/business metric — regular tourists see tourist-friendly metrics only.
    if st.session_state.get("admin_ok"):
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f'<div class="metric"><div class="v">{route.get("total_distance_km",0):,} km</div><div class="l">Distance</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric"><div class="v">{fmt_drive(route.get("total_duration_min",0))}</div><div class="l">Drive time</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric"><div class="v">SAR {route.get("estimated_cost",0):,}</div><div class="l">Est. cost</div></div>', unsafe_allow_html=True)
        m4.markdown(f'<div class="metric"><div class="v">{route.get("readiness",0)}%</div><div class="l">Readiness</div></div>', unsafe_allow_html=True)
    else:
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric"><div class="v">{route.get("total_distance_km",0):,} km</div><div class="l">Distance</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric"><div class="v">{fmt_drive(route.get("total_duration_min",0))}</div><div class="l">Drive time</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric"><div class="v">SAR {route.get("estimated_cost",0):,}</div><div class="l">Est. cost</div></div>', unsafe_allow_html=True)

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
                # Recommended stay (real hotels for this city)
                hotels = engine.hotels_for(s["destination_id"], t.get("budget_tier", "Mid-range"), t.get("accommodation"))
                if hotels:
                    st.markdown('<div class="sub" style="font-weight:700;color:#2f5233;margin-top:2px">🏨 Recommended stay</div>', unsafe_allow_html=True)
                    for h in hotels[:3]:
                        st.markdown(f'<div class="act"><span class="dotm"></span><span><b>{h[0]}</b> · {"★"*h[1]} · {h[2]} · ~SAR {h[3]}/night · {h[4]}</span></div>', unsafe_allow_html=True)
                # A schedule for EACH day of the stay
                days = engine.schedule_trip_days(s["destination_id"], s["nights"], t["day_start"], t["day_end"], t["pace"], t["cuisines"])
                for di, acts in enumerate(days, 1):
                    st.markdown(f'<div class="sub" style="font-weight:700;color:#2f5233;margin-top:10px">📅 Day {di}</div>', unsafe_allow_html=True)
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
                # notify the trip owner that a new member joined
                owner_email = t.get("owner_email") or ""
                if owner_email:
                    notifications.notify_member_joined(owner_email, t["owner_name"], name, t["title"])
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

    # ---- Vote on attractions & restaurants per chosen city ----
    st.markdown('<div class="sec">🎯 Vote on activities &amp; restaurants</div>', unsafe_allow_html=True)
    st.caption("For each city on the route, vote on the attractions and restaurants you'd like to include.")
    item_votes = db.get_item_votes(t["id"])
    for s in stops:
        did = s["destination_id"]
        with st.expander(f"📍 {s['name']} — activities & restaurants"):
            # Attractions
            st.markdown('<div class="sub" style="font-weight:700;color:#2f5233">🎟️ Attractions</div>', unsafe_allow_html=True)
            for a in data.attractions_for(did):
                aid, aname, acat, arating = a[0], a[2], a[3], a[6]
                c1, c2 = st.columns([3, 1])
                c1.markdown(f"**{aname}** · {acat} ★{arating}")
                ascore = c2.selectbox("Score", [1, 2, 3, 4, 5], index=4, key=f"at{did}{aid}", label_visibility="collapsed")
                if c2.button("Vote", key=f"atb{did}{aid}"):
                    db.add_item_vote(t["id"], st.session_state.member_id, did, "attraction", aid, aname, ascore)
                    st.toast(f"Voted {ascore} for {aname}")
                    st.rerun()
            # Restaurants
            st.markdown('<div class="sub" style="font-weight:700;color:#2f5233;margin-top:8px">🍽️ Restaurants</div>', unsafe_allow_html=True)
            for r in data.restaurants_for(did):
                rid, rname, rcui, rrating = r[0], r[2], r[3], r[6]
                c1, c2 = st.columns([3, 1])
                c1.markdown(f"**{rname}** · {data.CUISINE_LABELS.get(rcui, rcui)} ★{rrating}")
                rscore = c2.selectbox("Score", [1, 2, 3, 4, 5], index=4, key=f"rt{did}{rid}", label_visibility="collapsed")
                if c2.button("Vote", key=f"rtb{did}{rid}"):
                    db.add_item_vote(t["id"], st.session_state.member_id, did, "restaurant", rid, rname, rscore)
                    st.toast(f"Voted {rscore} for {rname}")
                    st.rerun()

    # ---- Group picks (top-voted activities & restaurants) ----
    if item_votes:
        st.markdown('<div class="sec">🏅 Group picks</div>', unsafe_allow_html=True)
        for s in stops:
            did = s["destination_id"]
            top = engine.rank_items_by_consensus(item_votes, destination_id=did)[:4]
            if not top:
                continue
            st.markdown(f"**{s['name']}**")
            for name, avg, cnt, itype in top:
                icon = "🎟️" if itype == "attraction" else "🍽️"
                st.progress(min(1.0, avg / 5), text=f"{icon} {name} — {avg}/5 ({cnt})")

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


# ============================================================ RECOMMENDATIONS
def page_recommendations():
    st.markdown('<div class="sec">✨ Personalized recommendations</div>', unsafe_allow_html=True)
    st.caption("We learn your taste from your past trips and suggest destinations you'll love.")

    name = st.text_input("Your name (as used in past trips)", st.session_state.member_name or "",
                         placeholder="e.g. Nada")
    if not name.strip():
        st.info("Enter your name to see recommendations based on your previous trips.")
        return

    past = db.trips_by_owner(name.strip()) + db.trips_with_member(name.strip())
    # de-duplicate by id
    seen, past_trips = set(), []
    for t in past:
        if t["id"] not in seen:
            seen.add(t["id"])
            past_trips.append(t)

    if not past_trips:
        st.warning(f"No past trips found for **{name}**. Create a trip first so we can learn your taste!")
        if st.button("✨ Create a trip", use_container_width=True):
            go("create")
        return

    past_interests = [t["interests"] for t in past_trips if t.get("interests")]
    visited = []
    for t in past_trips:
        visited += [s["destination_id"] for s in t["route"].get("stops", [])]
    taste = engine.aggregate_preferences(past_interests)

    st.markdown(f"**Your taste profile** (from {len(past_trips)} past trip(s))")
    cols = st.columns(len(taste) or 1)
    for i, (k, v) in enumerate(sorted(taste.items(), key=lambda x: -x[1])):
        cols[i % len(cols)].markdown(
            f'<div class="metric"><div class="v">{v:.1f}</div><div class="l">{data.INTEREST_LABELS.get(k,k)}</div></div>',
            unsafe_allow_html=True)

    st.markdown('<div class="sec">🎯 Recommended for you</div>', unsafe_allow_html=True)
    user_ratings = db.user_rec_ratings(name.strip())
    recs = engine.recommend_destinations(taste, visited_ids=visited, include_holy=False, limit=5,
                                         user_ratings=user_ratings)
    if not recs:
        st.info("You've explored everything! Try including holy cities or new interests.")
        return
    st.markdown('<div class="stagger">', unsafe_allow_html=True)
    for d, match, reason in recs:
        avg, cnt = db.rec_rating_summary(d["id"])
        stars_txt = f"⭐ {avg} ({cnt})" if cnt else "Not rated yet"
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <h3>{d['name']}</h3>
            <span class="pill">{match}% match</span>
          </div>
          <div class="sub">{d['region']} · {reason} · {stars_txt}</div>
          <p style="margin-top:8px">{d['blurb']}</p>
          <div>{"".join(f'<span class="tag">{h}</span>' for h in d['highlights'][:3])}</div>
        </div>""", unsafe_allow_html=True)

        # --- rating & feedback for this recommendation ---
        with st.expander(f"⭐ Rate & review {d['name']}", expanded=False):
            with st.form(f"rate_{d['id']}"):
                stars = st.slider("Your rating", 1, 5, 4, key=f"stars_{d['id']}")
                comment = st.text_area("Your review (optional)", key=f"cmt_{d['id']}",
                                       placeholder="What did you like or dislike?")
                if st.form_submit_button("Submit rating", use_container_width=True):
                    db.add_rec_rating(name.strip(), d["id"], stars, comment.strip())
                    st.success("Thanks! Your feedback improves future recommendations.")
                    st.rerun()
            for r in db.get_rec_ratings(d["id"])[:5]:
                st.markdown(
                    f'<div class="act"><span class="dotm"></span><span><b>{r["user_name"]}</b> '
                    f'— {"★"*r["stars"]}{"☆"*(5-r["stars"])}'
                    f'{f": {r["comment"]}" if r["comment"] else ""}</span></div>',
                    unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


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


# ============================================================ ADMIN DASHBOARD
def page_admin():
    st.markdown('<div class="sec">🔒 Admin Dashboard</div>', unsafe_allow_html=True)
    st.caption("Internal analytics — not visible in the public navigation.")

    # Password comes from Streamlit Secrets; a safe development fallback is used locally.
    expected = st.secrets.get("ADMIN_PASSWORD", "TRIPSA-ADMIN-2026")
    if not st.session_state.get("admin_ok", False):
        with st.form("admin_login"):
            pwd = st.text_input("Admin password", type="password")
            submitted = st.form_submit_button("Sign in", use_container_width=True)
        if submitted:
            if pwd == expected:
                st.session_state.admin_ok = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        return

    if st.button("Sign out", key="admin_logout"):
        st.session_state.admin_ok = False
        go("home")

    k = db.admin_overview()
    cols = st.columns(6)
    metrics = [
        ("Trips", k["trips"]), ("Members", k["members"]), ("Votes", k["votes"]),
        ("Comments", k["comments"]), ("Ratings", k["ratings"]),
        ("Avg rating", f'{k["avg_rating"]}★'),
    ]
    for c, (label, value) in zip(cols, metrics):
        c.metric(label, value)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec">📍 Most requested destinations</div>', unsafe_allow_html=True)
        demand = db.top_destinations_by_demand(10)
        if not demand:
            st.info("No trip demand data yet.")
        for rank, (did, count) in enumerate(demand, 1):
            dname = data.DEST_BY_ID.get(did, {}).get("name", did)
            st.markdown(f'<div class="act"><span class="dotm"></span><span><b>#{rank} {dname}</b> — {count} trip(s)</span></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec">⭐ Most reviewed destinations</div>', unsafe_allow_html=True)
        reviewed = db.top_destinations_by_reviews(10)
        if not reviewed:
            st.info("No recommendation reviews yet.")
        for rank, (did, count, avg) in enumerate(reviewed, 1):
            dname = data.DEST_BY_ID.get(did, {}).get("name", did)
            st.markdown(f'<div class="act"><span class="dotm"></span><span><b>#{rank} {dname}</b> — {avg}★ from {count}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec">📊 Rating distribution</div>', unsafe_allow_html=True)
    dist = db.rating_distribution()
    for stars in range(5, 0, -1):
        st.markdown(f"**{stars}★** — {dist[stars]} rating(s)")
        total = max(1, sum(dist.values()))
        st.progress(dist[stars] / total)


# ============================================================ Router
# top nav — native Streamlit buttons (reliable, no third-party widget state issues).
_nav_items = [("home","🏠 Home"),("create","✨ Create"),("join","🔑 Join"),("routes","🗺️ Routes"),("recommend","🎯 For You")]
_cols = st.columns(len(_nav_items))
for _i, (_p, _label) in enumerate(_nav_items):
    _active = (st.session_state.page == _p)
    if _cols[_i].button(_label, key=f"nav_{_p}", use_container_width=True,
                        type=("primary" if _active else "secondary")):
        go(_p)

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
elif page == "recommend":
    page_recommendations()
elif page == "admin":
    page_admin()

# Hidden admin entry — not part of the public nav. Lives in the sidebar.
with st.sidebar:
    st.markdown("### 🔐 Staff")
    if st.button("Admin dashboard", key="admin_entry", use_container_width=True):
        go("admin")
