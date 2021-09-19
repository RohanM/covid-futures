#!/usr/bin/env python3

from app import create_app, db

with create_app().app_context():
    db.create_all()
