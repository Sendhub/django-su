from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserSuFormTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username="formuser")

    def test_use_ajax_select_defaults_to_false(self):
        """use_ajax_select is False when ajax_select is not installed"""
        from django_su.forms import UserSuForm

        form = UserSuForm()
        self.assertFalse(form.use_ajax_select)

    def test_empty_submission_is_invalid(self):
        """Form with no data is invalid (user field is required)"""
        from django_su.forms import UserSuForm

        form = UserSuForm(data={})
        self.assertFalse(form.is_valid())

    def test_valid_submission(self):
        """Form with a valid user pk is valid"""
        from django_su.forms import UserSuForm

        form = UserSuForm(data={"user": self.user.pk})
        self.assertTrue(form.is_valid())

    def test_get_user_returns_user_instance(self):
        """get_user() returns the correct User object after validation"""
        from django_su.forms import UserSuForm

        form = UserSuForm(data={"user": self.user.pk})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_get_user_returns_none_after_failed_validation(self):
        """get_user() returns None when validation fails (required field missing)"""
        from django_su.forms import UserSuForm

        form = UserSuForm(data={})
        form.is_valid()  # sets cleaned_data even on failure
        self.assertIsNone(form.get_user())

    def test_nonexistent_user_is_invalid(self):
        """Form is invalid when the user pk does not exist"""
        from django_su.forms import UserSuForm

        form = UserSuForm(data={"user": 99999})
        self.assertFalse(form.is_valid())

    def test_non_integer_user_is_invalid(self):
        """Form is invalid when the user field is not an integer"""
        from django_su.forms import UserSuForm

        form = UserSuForm(data={"user": "notanumber"})
        self.assertFalse(form.is_valid())

    def test_str_returns_string(self):
        """__str__ returns an HTML string without raising"""
        from django_su.forms import UserSuForm

        form = UserSuForm()
        self.assertIsInstance(str(form), str)

    def test_user_field_is_required(self):
        """user field reports a validation error when missing"""
        from django_su.forms import UserSuForm

        form = UserSuForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("user", form.errors)

    def test_unbound_form_has_no_errors(self):
        """Unbound form (no data at all) has no validation errors"""
        from django_su.forms import UserSuForm

        form = UserSuForm()
        self.assertFalse(form.errors)
