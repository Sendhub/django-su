from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestSuBackend(TestCase):
    def setUp(self):
        super().setUp()
        from django_su.backends import SuBackend

        self.user = User.objects.create(username="testuser")
        self.backend = SuBackend()

    def test_authenticate_do_it(self):
        """Ensure authentication passes when su=True and user id is valid"""
        self.assertEqual(self.backend.authenticate(su=True, user_id=self.user.pk), self.user)

    def test_authenticate_dont_do_it(self):
        """Ensure authentication fails when su=False and user id is valid"""
        self.assertEqual(self.backend.authenticate(su=False, user_id=self.user.pk), None)

    def test_authenticate_id_none(self):
        """Ensure authentication fails when user_id is None"""
        self.assertEqual(self.backend.authenticate(su=True, user_id=None), None)

    def test_authenticate_id_non_existent(self):
        """Ensure authentication fails when user_id doesn't exist"""
        self.assertEqual(self.backend.authenticate(su=True, user_id=999), None)

    def test_authenticate_id_invalid(self):
        """Ensure authentication fails when user_id is invalid"""
        self.assertEqual(self.backend.authenticate(su=True, user_id="abc"), None)

    def test_get_user_exists(self):
        """Ensure get_user returns the expected user"""
        self.assertEqual(self.backend.get_user(user_id=self.user.pk), self.user)

    def test_get_user_does_not_exist(self):
        """Ensure get_user returns None if user is not found"""
        self.assertEqual(self.backend.get_user(user_id=999), None)

    def test_supports_inactive_user_is_false(self):
        """SuBackend does not support inactive users"""
        self.assertFalse(self.backend.supports_inactive_user)

    def test_authenticate_with_request_kwarg(self):
        """Ensure authentication passes when an explicit request object is provided"""
        from django.test import RequestFactory

        request = RequestFactory().get("/")
        self.assertEqual(self.backend.authenticate(request=request, su=True, user_id=self.user.pk), self.user)

    def test_authenticate_extra_kwargs_ignored(self):
        """Ensure extra keyword arguments do not raise errors"""
        result = self.backend.authenticate(su=True, user_id=self.user.pk, extra_kwarg="ignored")
        self.assertEqual(result, self.user)
