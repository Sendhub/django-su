import warnings

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


# Module-level callables for string-path import tests
def _always_true_callback(user):
    return True


def _always_false_callback(user):
    return False


_dummy_action_called = {"flag": False}


def _dummy_login_action(request, user):
    _dummy_action_called["flag"] = True


class SuLoginCallbackTest(TestCase):
    def setUp(self):
        super().setUp()
        self.superuser = User.objects.create(username="super", is_superuser=True)
        self.regular_user = User.objects.create(username="regular")

    def test_default_allows_superuser(self):
        """Default callback permits users with auth.change_user (superusers have all perms)"""
        from django_su.utils import su_login_callback

        self.assertTrue(su_login_callback(self.superuser))

    def test_default_denies_regular_user(self):
        """Default callback denies users without auth.change_user"""
        from django_su.utils import su_login_callback

        self.assertFalse(su_login_callback(self.regular_user))

    def test_callback_as_callable(self):
        """SU_LOGIN_CALLBACK callable is invoked and its result returned"""
        from django_su.utils import su_login_callback

        with self.settings(SU_LOGIN_CALLBACK=lambda u: True):
            self.assertTrue(su_login_callback(self.regular_user))

    def test_callback_as_callable_returns_false(self):
        """SU_LOGIN_CALLBACK callable returning False is respected"""
        from django_su.utils import su_login_callback

        with self.settings(SU_LOGIN_CALLBACK=lambda u: False):
            self.assertFalse(su_login_callback(self.superuser))

    def test_callback_as_string_path(self):
        """SU_LOGIN_CALLBACK as a dotted string is imported and called"""
        from django_su.utils import su_login_callback

        with self.settings(SU_LOGIN_CALLBACK="django_su.tests.test_utils._always_true_callback"):
            self.assertTrue(su_login_callback(self.regular_user))

    def test_callback_as_string_path_false(self):
        """SU_LOGIN_CALLBACK dotted string returning False is respected"""
        from django_su.utils import su_login_callback

        with self.settings(SU_LOGIN_CALLBACK="django_su.tests.test_utils._always_false_callback"):
            self.assertFalse(su_login_callback(self.superuser))

    def test_deprecated_su_login_emits_warning(self):
        """Presence of deprecated SU_LOGIN setting triggers DeprecationWarning"""
        from django_su.utils import su_login_callback

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            with self.settings(SU_LOGIN=True, SU_LOGIN_CALLBACK=None):
                su_login_callback(self.superuser)

        messages = [str(w.message) for w in caught]
        self.assertTrue(any("SU_LOGIN is deprecated" in m for m in messages))

    def test_no_deprecated_warning_without_su_login(self):
        """No DeprecationWarning when SU_LOGIN is absent"""
        from django_su.utils import su_login_callback

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            su_login_callback(self.superuser)

        dep_warnings = [w for w in caught if issubclass(w.category, DeprecationWarning)]
        self.assertFalse(dep_warnings)


class CustomLoginActionTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username="actionuser")

    def test_no_action_returns_false(self):
        """custom_login_action returns False when SU_CUSTOM_LOGIN_ACTION is not set"""
        from django_su.utils import custom_login_action

        with self.settings(SU_CUSTOM_LOGIN_ACTION=None):
            self.assertFalse(custom_login_action(None, self.user))

    def test_callable_action_is_invoked_and_returns_true(self):
        """custom_login_action calls the callable and returns True"""
        from django_su.utils import custom_login_action

        called = {"flag": False}

        def action(request, user):
            called["flag"] = True

        with self.settings(SU_CUSTOM_LOGIN_ACTION=action):
            result = custom_login_action(None, self.user)

        self.assertTrue(result)
        self.assertTrue(called["flag"])

    def test_callable_receives_request_and_user(self):
        """custom_login_action passes request and user to the callable"""
        from django_su.utils import custom_login_action

        received = {}

        def action(request, user):
            received["request"] = request
            received["user"] = user

        sentinel_request = object()
        with self.settings(SU_CUSTOM_LOGIN_ACTION=action):
            custom_login_action(sentinel_request, self.user)

        self.assertIs(received["request"], sentinel_request)
        self.assertEqual(received["user"], self.user)

    def test_string_action_is_imported_and_called(self):
        """custom_login_action imports a dotted-string callable and returns True"""
        from django_su.utils import custom_login_action

        _dummy_action_called["flag"] = False
        with self.settings(SU_CUSTOM_LOGIN_ACTION="django_su.tests.test_utils._dummy_login_action"):
            result = custom_login_action(None, self.user)

        self.assertTrue(result)
        self.assertTrue(_dummy_action_called["flag"])
