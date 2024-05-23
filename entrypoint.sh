#!/bin/sh

set -e

flask db init || true
flask db migrate -m "Initial migration" || true
flask db upgrade || true

exec flask run --host=0.0.0.0 --port=5000
