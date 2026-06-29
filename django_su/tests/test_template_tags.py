from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

User = get_user_model()


class LoginSuLinkTagTest(TestCase):
    def test_superuser_can_su(self):
        """login_su_link returns can_su_login=True for a superuser"""
        from django_su.templatetags.su_tags import login_su_link

        user = User.objects.create(username="supertaguser", is_superuser=True, is_staff=True)
        result = login_su_link(user)
        self.assertTrue(result["can_su_login"])

    def test_regular_user_cannot_su(self):
        """login_su_link returns can_su_login=False for a user with no permissions"""
        from django_su.templatetags.su_tags import login_su_link

        user = User.objects.create(username="regulartaguser")
        result = login_su_link(user)
        self.assertFalse(result["can_su_login"])

    def test_user_with_change_user_perm_can_su(self):
        """login_su_link returns can_su_login=True for a user with auth.change_user"""
        from django_su.templatetags.su_tags import login_su_link

        user = User.objects.create(username="permtaguser")
        ct = ContentType.objects.get_for_model(User)
        perm = Permission.objects.get(content_type=ct, codename="change_user")
        user.user_permissions.add(perm)
        # Reload to clear perm cache
        user = User.objects.get(pk=user.pk)
        result = login_su_link(user)
        self.assertTrue(result["can_su_login"])

    def test_returns_dict_with_can_su_login_key(self):
        """login_su_link always returns a dict containing can_su_login"""
        from django_su.templatetags.su_tags import login_su_link

        user = User.objects.create(username="dicttaguser")
        result = login_su_link(user)
        self.assertIn("can_su_login", result)

    def test_custom_callback_controls_access(self):
        """login_su_link respects SU_LOGIN_CALLBACK"""
        from django_su.templatetags.su_tags import login_su_link

        user = User.objects.create(username="cbtaguser")
        with self.settings(SU_LOGIN_CALLBACK=lambda u: True):
            result = login_su_link(user)
        self.assertTrue(result["can_su_login"])
