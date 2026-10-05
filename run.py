#!/usr/bin/env python3
"""BAM Studio application entry point."""
import os
import sys

# Ensure project root is on sys.path (fixes ModuleNotFoundError: app)
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT, ".env"))

from app import create_app, db
from app.services.seed import run_seed

# Flask application instance (name must be `app` for Vercel / WSGI)
app = create_app(os.environ.get("FLASK_ENV", "development"))


# CLI commands only when running under Flask CLI (not required on Vercel)
if hasattr(app, "cli"):
    @app.cli.command("seed")
    def seed_command():
        """Seed database with initial data."""
        run_seed()

    @app.cli.command("init-db")
    def init_db():
        """Create all tables and seed."""
        db.create_all()
        run_seed()
        print("Database initialized.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
