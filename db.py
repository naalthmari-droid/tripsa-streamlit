"""TRIPSA — SQLite persistence for trips, members, preferences, votes, comments."""
import json
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "tripsa.db")


def _conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS trips(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, owner_name TEXT, owner_age INTEGER,
        invite_code TEXT UNIQUE, start_destination_id TEXT,
        start_date TEXT, end_date TEXT, travelers INTEGER,
        budget_tier TEXT, pace TEXT, is_group INTEGER,
        include_holy INTEGER, interests TEXT, audience TEXT,
        route_mode TEXT, certified_route_id TEXT, cuisines TEXT,
        accommodation TEXT, day_start INTEGER, day_end INTEGER,
        route_json TEXT, status TEXT, created_at TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS members(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id INTEGER, name TEXT, age INTEGER,
        preferences TEXT, joined_at TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS votes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id INTEGER, member_id INTEGER, destination_id TEXT, score INTEGER)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS comments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id INTEGER, member_name TEXT, destination_id TEXT,
        body TEXT, created_at TEXT)""")
    conn.commit()
    conn.close()


def create_trip(t):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""INSERT INTO trips(title,owner_name,owner_age,invite_code,start_destination_id,
        start_date,end_date,travelers,budget_tier,pace,is_group,include_holy,interests,audience,
        route_mode,certified_route_id,cuisines,accommodation,day_start,day_end,route_json,status,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (t["title"], t["owner_name"], t.get("owner_age"), t["invite_code"], t["start_destination_id"],
         t["start_date"], t["end_date"], t["travelers"], t["budget_tier"], t["pace"],
         int(t["is_group"]), int(t["include_holy"]), json.dumps(t["interests"]), t["audience"],
         t["route_mode"], t.get("certified_route_id"), json.dumps(t.get("cuisines", [])),
         t.get("accommodation"), t["day_start"], t["day_end"], json.dumps(t["route"]),
         "active", datetime.utcnow().isoformat()))
    tid = cur.lastrowid
    conn.commit()
    conn.close()
    return tid


def get_trip(tid):
    conn = _conn()
    row = conn.execute("SELECT * FROM trips WHERE id=?", (tid,)).fetchone()
    conn.close()
    return _trip_dict(row) if row else None


def get_trip_by_code(code):
    conn = _conn()
    row = conn.execute("SELECT * FROM trips WHERE invite_code=?", (code,)).fetchone()
    conn.close()
    return _trip_dict(row) if row else None


def list_trips():
    conn = _conn()
    rows = conn.execute("SELECT * FROM trips ORDER BY id DESC").fetchall()
    conn.close()
    return [_trip_dict(r) for r in rows]


def trips_by_owner(owner_name):
    """All trips created by a given owner name (past trips for recommendations)."""
    conn = _conn()
    rows = conn.execute("SELECT * FROM trips WHERE owner_name=? ORDER BY id DESC", (owner_name,)).fetchall()
    conn.close()
    return [_trip_dict(r) for r in rows]


def trips_with_member(member_name):
    """Trips where this name appears as a member (to learn their taste)."""
    conn = _conn()
    rows = conn.execute(
        "SELECT DISTINCT t.* FROM trips t JOIN members m ON m.trip_id=t.id WHERE m.name=? ORDER BY t.id DESC",
        (member_name,)).fetchall()
    conn.close()
    return [_trip_dict(r) for r in rows]


def _trip_dict(row):
    d = dict(row)
    d["interests"] = json.loads(d.get("interests") or "{}")
    d["cuisines"] = json.loads(d.get("cuisines") or "[]")
    d["route"] = json.loads(d.get("route_json") or "{}")
    return d


def add_member(trip_id, name, age, preferences):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO members(trip_id,name,age,preferences,joined_at) VALUES(?,?,?,?,?)",
                (trip_id, name, age, json.dumps(preferences), datetime.utcnow().isoformat()))
    mid = cur.lastrowid
    conn.commit()
    conn.close()
    return mid


def get_members(trip_id):
    conn = _conn()
    rows = conn.execute("SELECT * FROM members WHERE trip_id=? ORDER BY id", (trip_id,)).fetchall()
    conn.close()
    out = []
    for r in rows:
        d = dict(r)
        d["preferences"] = json.loads(d.get("preferences") or "{}")
        out.append(d)
    return out


def add_vote(trip_id, member_id, destination_id, score):
    conn = _conn()
    conn.execute("INSERT INTO votes(trip_id,member_id,destination_id,score) VALUES(?,?,?,?)",
                 (trip_id, member_id, destination_id, score))
    conn.commit()
    conn.close()


def get_votes(trip_id):
    conn = _conn()
    rows = conn.execute("SELECT * FROM votes WHERE trip_id=?", (trip_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_comment(trip_id, member_name, destination_id, body):
    conn = _conn()
    conn.execute("INSERT INTO comments(trip_id,member_name,destination_id,body,created_at) VALUES(?,?,?,?,?)",
                 (trip_id, member_name, destination_id, body, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()


def get_comments(trip_id):
    conn = _conn()
    rows = conn.execute("SELECT * FROM comments WHERE trip_id=? ORDER BY id DESC", (trip_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
