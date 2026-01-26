# bicycledata

Lightweight web application for collecting and inspecting bicycle sensor
and traffic data. Provides a small web UI and APIs for managing devices,
user sessions and recorded traffic events. Documentation and design
notes are in the `bicycledata/docs/` folder.

Key points
- Framework: Flask (WSGI entrypoint at `wsgi.py`)
- Docs: see [bicycledata/docs](bicycledata/docs)

Quick start (development)
1. Create a virtualenv and install dependencies:

   python3 -m venv .env
   .env/bin/pip install -r requirements.txt

2. Run the app locally:

   .env/bin/python wsgi.py

For production deployment, use a WSGI server (uWSGI/gunicorn) and a
reverse proxy (nginx).

Questions or contributions: open an issue or pull request.
