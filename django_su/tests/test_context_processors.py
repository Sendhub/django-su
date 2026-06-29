from django.test import RequestFactory, TestCase

from django_su.context_processors import is_su


class FakeSession(dict):
    """Minimal session-like dict that accepts `default` as a keyword arg, matching Django's SessionBase.get."""

    def get(self, key, default=None):
        return super().get(key, default)


class IsSubContextProcessorTest(TestCase):
    def setUp(self):
        super().setUp()
        self.request = RequestFactory().get("/")

    def _with_session(self, data):
        self.request.session = FakeSession(data)

    def test_returns_dict_with_is_su_key(self):
        """is_su always returns a dict containing IS_SU"""
        self._with_session({})
        result = is_su(self.request)
        self.assertIn("IS_SU", result)

    def test_not_su_when_key_absent(self):
        """IS_SU is 0 when exit_users_pk is not in the session"""
        self._with_session({})
        self.assertEqual(is_su(self.request)["IS_SU"], 0)

    def test_not_su_when_list_empty(self):
        """IS_SU is 0 when exit_users_pk is an empty list"""
        self._with_session({"exit_users_pk": []})
        self.assertEqual(is_su(self.request)["IS_SU"], 0)

    def test_is_su_single_entry(self):
        """IS_SU is 1 when one su entry exists"""
        self._with_session({"exit_users_pk": [["1", "backend"]]})
        self.assertEqual(is_su(self.request)["IS_SU"], 1)

    def test_is_su_multiple_entries(self):
        """IS_SU equals the number of nested su entries"""
        self._with_session({"exit_users_pk": [["1", "b1"], ["2", "b2"], ["3", "b3"]]})
        self.assertEqual(is_su(self.request)["IS_SU"], 3)

    def test_is_su_value_is_integer(self):
        """IS_SU is an int (len of list), not a bool"""
        self._with_session({"exit_users_pk": [["1", "b1"], ["2", "b2"]]})
        result = is_su(self.request)
        self.assertIsInstance(result["IS_SU"], int)
        self.assertEqual(result["IS_SU"], 2)
