from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py", default_timeout=30)
at.run()
print("initial page:", at.session_state.page)
print("buttons found:", [b.label for b in at.button][:8])

# click the Create nav button
for b in at.button:
    if b.label == "✨ Create":
        b.click().run()
        break
print("after clicking Create, page:", at.session_state.page)
assert at.session_state.page == "create", "NAV FAILED: still on " + at.session_state.page
print("NAV TO CREATE: OK ✓")

# check create page rendered (look for the form submit button)
labels = [b.label for b in at.button]
print("create page buttons:", labels[:10])
has_generate = any("Generate" in (l or "") for l in labels)
print("Generate button present:", has_generate)
