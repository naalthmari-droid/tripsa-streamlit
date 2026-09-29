# TRIPSA TODO

- [x] Create a new Turso database in a region close to Streamlit Cloud (US) instead of Tokyo
- [x] Migrate all existing trip data to the new database and verify counts match
- [x] Update TURSO_URL and TURSO_TOKEN in Streamlit Cloud secrets and reboot the app
- [x] Verify app speed improvement after the region move
- [x] Add founders table with unique username and securely hashed password
- [x] Add founder_id ownership field to trips with backward-compatible migration
- [x] Implement founder registration, login, logout, and session handling
- [x] Restrict trip creation to logged-in founders
- [x] Add My Trips page showing only the logged-in founder's trip history
- [x] Keep invite-link members isolated from founder account and other trips
- [x] Add tests for authentication, ownership isolation, and invite-member access
- [x] Publish the update to GitHub and Streamlit Cloud
- [x] Rotate Turso secrets: revoke exposed platform token, issue new DB token, update Streamlit secrets, verify app healthy
- [x] Custom activity: any member can add a custom activity/event (name, city, type, cost, duration, link) to the trip room before finalization
- [x] Custom activities appear for all members and are votable like built-in items
- [x] Approved custom activities are included in the regenerated Final Plan schedule
- [x] Member who added a custom activity can delete it before finalization
- [x] Merge Almosaferoon scraped data: add 5 new destinations (Umluj, KAEC, Jazan, Farasan, Tanomah) + ~45 new attractions
- [x] Enrich existing destinations with recommended stay duration, best visit months, and planning rules
- [x] Map Arabic attraction categories to app interest keys for recommendations/scheduling
- [x] Test recommendations, scheduling, voting with merged data and publish

## Scheduling uniqueness hardening — 2026-09-17

- [x] Remove the exhausted-pool fallback that reintroduces previously used attractions
- [x] Deduplicate by stable ID and normalized city/name, distribute remaining choices across days, and track only scheduled activities
- [x] Preserve the scheduler call signature and existing custom-activity pinning behavior; show free time when no unique activity fits
- [x] Add regression tests for scarce/empty/duplicate data, long stays, short windows, cache isolation, and current destinations
- [x] Run syntax checks and isolated Streamlit AppTest

Validation: `python3 -m unittest discover -s tests -v` passes 20 tests, including 480 schedule combinations across 20 destinations. The matrix covers 1/4/14/30 days, all three paces, and two waking-hour windows. AppTest verifies Home, Detail, Shared Schedule and Final Plan; pins remain at 16:00 on days 2 and 30. An exhausted day's free-time placeholder is replaced when a pinned event is added. PDF extraction verifies all 30 days, unique catalog activities and explicit free time. Install test-only dependencies with `pip install -r requirements-dev.txt`. All integration-test writes use a temporary SQLite database, not Turso or the existing local database.

Scope: uniqueness is per city stay for catalog attractions, by ID or normalized city/name, not fuzzy multilingual alias matching. Restaurant choices may recur. Existing custom-activity approval rules and storage remain unchanged. The Final Plan now removes rows that overlap a member-pinned activity. Unified custom-activity scheduling/PDF export remains a separate follow-up.

## Geographic daily scheduling + judging deck expansion — 2026-09-30

- [x] Order attractions with valid coordinates by a city-seeded nearest-neighbor path.
- [x] Preserve that order when splitting attractions across stay days, while retaining no-repeat and time-window guarantees.
- [x] Add regression coverage for same-day geographic clustering and run the complete suite: 20 tests passed.
- [x] Capture local UI evidence for member-suggested activities, group voting, pinned time, and final-plan inclusion.
- [x] Expand the Arabic judging deck with the previous five-step journey slide, activity-voting flow, spatial optimization, future concierge package, and logo story.

## Premium UI redesign — 2026-09-30

- [x] Replace the visual system with a bold pine, mint, purple and gold App Store-style palette.
- [x] Rebuild the home hero around the TRIPSA identity and a realistic itinerary preview.
- [x] Unify cards, forms, navigation, itinerary rows, alerts and sidebar surfaces.
- [x] Verify desktop/mobile readability, existing flows and the full automated test suite.
- [ ] Publish the redesign to GitHub main and verify the live health endpoint.
