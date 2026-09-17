"""UI/PDF integration tests using only a temporary local SQLite database."""
import io
from pathlib import Path
import tempfile
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from pypdf import PdfReader
import streamlit as st
from streamlit.testing.v1 import AppTest

import data
import db
import engine
import pdf_export

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class ScheduleIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="tripsa-scheduler-test-")
        self.addCleanup(self.tmp.cleanup)
        self.creds = patch.object(db, "_creds", return_value=("", ""))
        self.path = patch.object(db, "DB_PATH", str(Path(self.tmp.name) / "test.db"))
        self.creds.start()
        self.path.start()
        self.addCleanup(self.creds.stop)
        self.addCleanup(self.path.stop)
        self.addCleanup(st.cache_data.clear)
        self.addCleanup(st.cache_resource.clear)
        st.cache_data.clear()
        st.cache_resource.clear()
        db.init_db()
        start = datetime(2026, 12, 1)
        end = start + timedelta(days=30)
        interests = {key: 3 for key in data.INTEREST_LABELS}
        route = engine.build_optimized_route("riyadh", ["riyadh"], interests,
                                             start, end, 2, 500, "moderate", False)
        self.trip_id = db.create_trip(dict(
            title="Scheduler regression test", owner_name="Local tester", owner_age=30,
            owner_email="", invite_code="TRP-TESTA", start_destination_id="riyadh",
            start_date=start.date().isoformat(), end_date=end.date().isoformat(),
            travelers=2, budget_tier="Mid-range", pace="moderate", is_group=True,
            include_holy=False, interests=interests, audience="tourist", route_mode="custom",
            cuisines=[], accommodation="Mid-range (3-4★ hotel)", day_start=9, day_end=22,
            route=route))
        self.member_id = db.add_member(self.trip_id, "Local tester", 30, interests)

    def open_page(self, page):
        at = AppTest.from_file(str(APP_PATH), default_timeout=30)
        at.session_state["page"] = page
        at.session_state["trip_id"] = self.trip_id
        at.session_state["member_id"] = self.member_id
        at.session_state["member_name"] = "Local tester"
        at.run()
        self.assertEqual(len(at.exception), 0, [exc.message for exc in at.exception])
        return at

    def test_home_and_detail_render_all_days_and_free_time(self):
        self.open_page("home")
        at = self.open_page("detail")
        schedule = next(e for e in at.expander if "Day schedule" in e.label)
        html = "\n".join(item.value for item in schedule.markdown)
        self.assertIn("Day 30", html)
        self.assertIn("Free time", html)
        self.assertEqual(html.count("National Museum"), 1)

    def test_shared_and_final_schedules_are_unique_and_pin_stays_at_chosen_time(self):
        custom_id = db.add_custom_item(self.trip_id, self.member_id, "Local tester",
                                       "riyadh", "Regression group event", duration_min=60,
                                       pref_day=2, pref_time_min=960)
        late_id = db.add_custom_item(self.trip_id, self.member_id, "Local tester",
                                     "riyadh", "Last-day group event", duration_min=60,
                                     pref_day=30, pref_time_min=960)
        db.save_item_votes(self.trip_id, self.member_id,
                           [("riyadh", "custom", f"c{custom_id}", "Regression group event", 5),
                            ("riyadh", "custom", f"c{late_id}", "Last-day group event", 5)])
        db.mark_plan_finalized(self.trip_id, True)
        at = self.open_page("room")
        schedules = [e for e in at.expander if "Day schedule" in e.label]
        self.assertEqual(len(schedules), 2, "Shared schedule and Final Plan")
        for schedule in schedules:
            html = "\n".join(item.value for item in schedule.markdown)
            self.assertIn("Day 30", html)
            self.assertIn("Free time", html)
            self.assertEqual(html.count("National Museum"), 1)
        final_html = "\n".join(item.value for item in schedules[1].markdown)
        self.assertEqual(final_html.count("Regression group event"), 1)
        day_two = final_html.split("Day 2</div>")[1].split("Day 3</div>")[0]
        self.assertIn("16:00–17:00", day_two)
        self.assertIn("Regression group event", day_two)
        day_thirty = final_html.split("Day 30</div>")[1]
        self.assertIn("16:00–17:00", day_thirty)
        self.assertIn("Last-day group event", day_thirty)
        self.assertNotIn("Free time", day_thirty)
        self.assertFalse(any("PDF unavailable" in caption.value for caption in at.caption))
        self.assertEqual(len(at.get("download_button")), 1)
        # Cached base schedule must not acquire a custom activity on the next render.
        at.run()
        self.assertEqual(len(at.exception), 0)
        schedules = [e for e in at.expander if "Day schedule" in e.label]
        self.assertNotIn("Regression group event", "\n".join(m.value for m in schedules[0].markdown))

    def test_pdf_uses_same_unique_catalog_schedule_and_keeps_free_days(self):
        trip = db.get_trip(self.trip_id)
        payload = pdf_export.build_final_plan_pdf(trip, db.get_members(self.trip_id))
        self.assertTrue(payload.startswith(b"%PDF-"))
        reader = PdfReader(io.BytesIO(payload))
        text = "\n".join(page.extract_text() for page in reader.pages)
        self.assertIn("Day 30", text)
        self.assertIn("Free time", text)
        self.assertEqual(text.count("National Museum"), 1)
        print(f"PDF regression passed: {len(reader.pages)} pages; unique catalog activities and free-time days preserved.")


if __name__ == "__main__":
    unittest.main()
