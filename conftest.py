import os
import sys

# test_settings.py lives in tests/ — add it to the path so Django can import it.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tests"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
