#!/usr/bin/env python3

from app import create_app

with create_app().app_context():
    db.create_all()
