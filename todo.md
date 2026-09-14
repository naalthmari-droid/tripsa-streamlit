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
