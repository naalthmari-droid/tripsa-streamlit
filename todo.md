# TRIPSA TODO

- [ ] Create a new Turso database in a region close to Streamlit Cloud (US) instead of Tokyo
- [ ] Migrate all existing trip data to the new database and verify counts match
- [ ] Update TURSO_URL and TURSO_TOKEN in Streamlit Cloud secrets and reboot the app
- [ ] Verify app speed improvement after the region move
- [ ] Add founders table with unique username and securely hashed password
- [ ] Add founder_id ownership field to trips with backward-compatible migration
- [ ] Implement founder registration, login, logout, and session handling
- [ ] Restrict trip creation to logged-in founders
- [ ] Add My Trips page showing only the logged-in founder's trip history
- [ ] Keep invite-link members isolated from founder account and other trips
- [ ] Add tests for authentication, ownership isolation, and invite-member access
- [ ] Publish the update to GitHub and Streamlit Cloud
