#!venv/bin/python
from app import app
#app.run(debug=True, host='0.0.0.0')
app.run(debug=True, host='0.0.0.0', use_reloader=False)
