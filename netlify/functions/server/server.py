"""
Netlify Functions entrypoint: AWS Lambda–shaped event → WSGI → Flask.

Requires dependency: serverless-wsgi (see requirements.txt in this folder).
"""
from __future__ import annotations

import os
import sys

from serverless_wsgi import handle_request

_here = os.path.dirname(os.path.abspath(__file__))
# In production Netlify zips included_files at the artifact root next to this folder
# (e.g. /var/task/app.py + /var/task/server/server.py). Locally in git it's three levels up.
_candid = os.path.abspath(os.path.join(_here, ".."))
if os.path.isfile(os.path.join(_candid, "app.py")):
    _ROOT = _candid
else:
    _ROOT = os.path.abspath(os.path.join(_here, "..", "..", ".."))

if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

from app import app as flask_app  # noqa: E402


def handler(event, context):
    """Lambda-compatible handler invoked by Netlify for each HTTP request."""
    return handle_request(flask_app, event, context)
