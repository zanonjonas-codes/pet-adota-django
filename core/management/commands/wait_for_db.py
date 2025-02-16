"""
Django command to wait for the database to be available.
"""
import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from psycopg2 import OperationalError as PsycopgOperationalError


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]

                db_name = db_conn.settings_dict["NAME"]
                db_host = db_conn.settings_dict["HOST"]
                self.stdout.write(f"db name is = {db_name} and host = {db_host}")

            except (OperationalError, PsycopgOperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
