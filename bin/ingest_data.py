#!/usr/bin/env python3

from app import create_app
from app.lib.data_ingester import DataIngester

with create_app().app_context():
    ingester = DataIngester()
    ingester.ingest()
