"""Regression tests for per-stay activity uniqueness; no network or live DB."""
import copy
import unittest
from unittest.mock import patch

import data
import engine


def attraction(aid, name=None, duration=60, category="Museum", lat=24.0, lng=46.0):
    return (aid, "test_city", name or f"Place {aid}", category, lat, lng, 4.5, 1, duration)


def activities(days):
    return [row for day in days for row in day if row["kind"] == "activity"]


def minute(value):
    hour, minutes = map(int, value.split(":"))
    return hour * 60 + minutes


class ScheduleTests(unittest.TestCase):
    def setUp(self):
        engine.schedule_trip_days.clear()

    def tearDown(self):
        engine.schedule_trip_days.clear()

    def generate(self, attrs, days=5, start=9, end=22, pace="moderate"):
        with patch.object(engine, "attractions_for", return_value=attrs), patch.object(
            engine, "restaurants_by_cuisines", return_value=[]
        ):
            return engine.schedule_trip_days("test_city", days, start, end, pace, [])

    def assert_unique(self, days):
        rows = activities(days)
        ids = [row["item_id"] for row in rows]
        names = [" ".join(row["label"].casefold().split()) for row in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(names), len(set(names)))

    def test_scarce_catalog_never_refills_with_used_activities(self):
        days = self.generate([attraction("only")], days=5)
        self.assertEqual(len(days), 5)
        self.assertEqual(len(activities(days)), 1)
        self.assert_unique(days)
        self.assertTrue(all(day and day[0]["kind"] == "free_time" for day in days[1:]))

    def test_empty_catalog_is_free_time_not_division_by_zero(self):
        days = self.generate([], days=3)
        self.assertEqual(len(days), 3)
        self.assertEqual(activities(days), [])
        for day in days:
            self.assertEqual(day[0]["kind"], "free_time")
            self.assertEqual((day[0]["time"], day[0]["end"]), ("09:00", "22:00"))

    def test_duplicate_ids_are_removed(self):
        rows = [attraction("same", "First name"), attraction("same", "Alias"), attraction("other")]
        result = self.generate(rows, days=3)
        self.assertEqual(len(activities(result)), 2)
        self.assert_unique(result)

    def test_duplicate_normalized_names_with_different_ids_are_removed(self):
        rows = [attraction("one", "National Museum"), attraction("two", "  NATIONAL   MUSEUM "),
                attraction("three", "ﻣﺘﺤﻒ"), attraction("four", "متحف")]
        result = self.generate(rows, days=4)
        self.assertEqual(len(activities(result)), 2)
        self.assert_unique(result)

    def test_equal_distribution_does_not_discard_extra_pool_candidates(self):
        rows = [attraction(str(i)) for i in range(12)]
        result = self.generate(rows, days=4)
        self.assertEqual([len(activities([day])) for day in result], [3, 3, 3, 3])
        self.assertEqual(len(activities(result)), 12)
        self.assert_unique(result)

    def test_same_day_activities_follow_nearby_geographic_clusters(self):
        rows = [
            attraction("near_a", lat=24.01, lng=46.01),
            attraction("far_a", lat=25.00, lng=47.00),
            attraction("near_b", lat=24.02, lng=46.02),
            attraction("far_b", lat=25.01, lng=47.01),
        ]
        with patch.dict(engine.DEST_BY_ID, {
            "test_city": {"lat": 24.0, "lng": 46.0}
        }), patch.object(engine, "attractions_for", return_value=rows), patch.object(
            engine, "restaurants_by_cuisines", return_value=[]
        ):
            result = engine.schedule_trip_days("test_city", 2, 9, 22, "moderate", [])
        day_ids = [[row["item_id"] for row in day if row["kind"] == "activity"] for day in result]
        self.assertEqual(day_ids, [["near_a", "near_b"], ["far_a", "far_b"]])

    def test_unused_candidates_remain_available_for_later_days(self):
        rows = [attraction(str(i), duration=60) for i in range(8)]
        result = self.generate(rows, days=2, start=9, end=11)
        self.assertEqual([len(activities([day])) for day in result], [1, 1])
        self.assertEqual([row["item_id"] for row in activities(result)], ["0", "1"])

    def test_oversized_candidate_does_not_block_shorter_fitting_activity(self):
        rows = [attraction("long", duration=600), attraction("short", duration=60)]
        result = self.generate(rows, days=1, start=9, end=11)
        self.assertEqual([row["item_id"] for row in activities(result)], ["short"])

    def test_nothing_fits_yields_free_time(self):
        result = self.generate([attraction("long", duration=600)], days=2, start=9, end=11)
        self.assertEqual(activities(result), [])
        self.assertTrue(all(day[0]["kind"] == "free_time" for day in result))

    def test_pace_limit_is_preserved(self):
        rows = [attraction(str(i), duration=30) for i in range(20)]
        for pace, limit in [("relaxed", 3), ("moderate", 4), ("action_packed", 5)]:
            with self.subTest(pace=pace):
                result = self.generate(rows, days=1, pace=pace)
                self.assertEqual(len(activities(result)), limit)

    def test_cache_is_deterministic_and_mutation_isolated(self):
        rows = [attraction(str(i)) for i in range(12)]
        expected = self.generate(rows, days=4)
        changed = self.generate(rows, days=4)
        changed[0].append({"label": "Custom pinned activity", "kind": "activity"})
        again = self.generate(rows, days=4)
        self.assertEqual(expected, again)

    def test_source_catalog_is_not_mutated(self):
        rows = [attraction(str(i)) for i in range(7)]
        original = copy.deepcopy(rows)
        self.generate(rows)
        self.assertEqual(rows, original)

    def test_numeric_strings_from_storage_are_supported(self):
        rows = [attraction(str(i)) for i in range(7)]
        result = self.generate(rows, days="4", start="9", end="22")
        self.assertEqual(len(result), 4)
        self.assert_unique(result)

    def test_existing_pinned_helper_contract_is_preserved(self):
        with patch.object(engine, "restaurants_by_cuisines", return_value=[]):
            result = engine._schedule_one_day("test_city", 9, 22, "moderate", [],
                                             [attraction("morning")], 2,
                                             pinned=[{"label": "Group event", "minutes": 960, "dur": 60}])
        pinned = [row for row in result if row.get("pinned")]
        self.assertEqual(len(pinned), 1)
        self.assertEqual(pinned[0]["time"], "16:00")

    def test_inserting_pinned_activity_removes_time_conflicts(self):
        base = [
            {"time": "14:40", "end": "16:10", "label": "Place A", "kind": "activity"},
            {"time": "16:40", "end": "18:10", "label": "Place B", "kind": "activity"},
            {"time": "19:00", "end": "20:00", "label": "Dinner", "kind": "meal"},
        ]
        result = engine.insert_pinned_activity(base, "Group event", 16 * 60, 120)
        self.assertEqual([row["label"] for row in result], ["Group event", "Dinner"])
        self.assertEqual((result[0]["time"], result[0]["end"]), ("16:00", "18:00"))

    def test_meals_do_not_extend_past_day_end(self):
        with patch.object(engine, "attractions_for", return_value=[attraction("a", duration=30)]), patch.object(
            engine, "restaurants_by_cuisines", return_value=[attraction("meal", duration=90)]
        ):
            result = engine.schedule_trip_days("test_city", 1, 12, 13, "moderate", [])
        for row in result[0]:
            self.assertLessEqual(minute(row["end"]), 13 * 60)

    def test_current_destinations_stays_paces_and_windows(self):
        cases = 0
        for did in data.DEST_BY_ID:
            for count in (1, 4, 14, 30):
                for pace in ("relaxed", "moderate", "action_packed"):
                    for start, end in ((9, 22), (12, 18)):
                        with self.subTest(city=did, days=count, pace=pace, window=(start, end)):
                            result = engine.schedule_trip_days(did, count, start, end, pace, [])
                            self.assertEqual(len(result), count)
                            self.assert_unique(result)
                            for day in result:
                                self.assertTrue(day, "Each day must have a schedule or explicit free time")
                                previous_end = start * 60
                                for row in day:
                                    self.assertGreaterEqual(minute(row["time"]), previous_end)
                                    self.assertLessEqual(minute(row["end"]), end * 60)
                                    self.assertGreater(minute(row["end"]), minute(row["time"]))
                                    previous_end = minute(row["end"])
                            cases += 1
        print(f"Validated {cases} real-catalog schedule combinations across {len(data.DEST_BY_ID)} destinations.")


if __name__ == "__main__":
    unittest.main()
