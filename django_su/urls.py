from django.urls import re_path  # use path if simpler patterns are preferred

from .views import login_as_user, su_login, su_logout

urlpatterns = [
    re_path(r"^$", su_logout, name="su_logout"),
    re_path(r"^login/$", su_login, name="su_login"),
    re_path(r"^(?P<user_id>-?[\d]+)/$", login_as_user, name="login_as_user"),
]
