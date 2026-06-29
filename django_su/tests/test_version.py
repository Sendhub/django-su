from unittest.mock import patch

from django.test import TestCase


class VersionTest(TestCase):
    def test_version_is_string(self):
        from django_su.version import VERSION

        self.assertIsInstance(VERSION, str)

    def test_get_version_returns_string(self):
        from django_su.version import get_version

        self.assertIsInstance(get_version(), str)

    def test_get_version_matches_version_constant(self):
        from django_su import version

        self.assertEqual(version.VERSION, version.get_version())

    def test_get_version_fallback_when_file_missing(self):
        from django_su import version

        with patch("pathlib.Path.read_text", side_effect=FileNotFoundError("no file")):
            result = version.get_version()
        self.assertEqual(result, "1.0.0")

    def test_get_version_fallback_when_content_malformed(self):
        from django_su import version

        with patch("pathlib.Path.read_text", return_value="not-a-version!!!"):
            result = version.get_version()
        self.assertEqual(result, "1.0.0")
