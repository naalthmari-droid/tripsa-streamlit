from streamlit.testing.v1 import AppTest
import os
if os.path.exists('tripsa.db'): os.remove('tripsa.db')
at=AppTest.from_file('app.py', default_timeout=60).run()
# Navigate Create
next(b for b in at.button if b.label=='✨ Create').click().run()
print('page after nav:', at.session_state.page)
# fill title/name; default dates are valid and other fields have defaults
texts=list(at.text_input)
print('text fields:', [x.label for x in texts])
for x in texts:
    if x.label=='Trip title': x.input('UI E2E Trip')
    if x.label=='Your name': x.input('Nada')
# generate
next(b for b in at.button if 'Generate optimized route' in b.label).click().run()
print('page after generate:', at.session_state.page)
print('trip_id:', at.session_state.trip_id)
assert at.session_state.page=='detail'
assert at.session_state.trip_id is not None
# verify rendered page contains title/code
alltext=' '.join([m.value for m in at.markdown])
print('title rendered:', 'UI E2E Trip' in alltext)
print('invite rendered:', 'TRP-' in alltext)
print('FULL UI CREATE FLOW PASSED ✓')
