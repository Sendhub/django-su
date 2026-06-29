django-su
=========

Login as any user from the Django admin interface, then switch back when done.

[![PyPI version](https://img.shields.io/pypi/v/django-su.svg)](https://pypi.python.org/pypi/django-su/)
[![Downloads](https://img.shields.io/pypi/dm/django-su.svg)](https://pypi.python.org/pypi/django-su/)
[![License](https://img.shields.io/github/license/adamcharnock/django-su.svg)](https://pypi.python.org/pypi/django-su/)

Table Of Contents
-----------------

- [django-su](#django-su)
  - [Table Of Contents](#table-of-contents)
  - [About](#about)
  - [What's New](#whats-new)
    - [Version 1.0.0 (Latest)](#version-100-latest)
    - [Python Packaging Migration](#python-packaging-migration)
    - [Extended Django and Python Support](#extended-django-and-python-support)
  - [Installation](#installation)
    - [External dependencies (optional, but recommended)](#external-dependencies-optional-but-recommended)
  - [Building & Packaging](#building--packaging)
  - [Testing The Build](#testing-the-build)
  - [Development Workflow](#development-workflow)
  - [Configuration (Optional)](#configuration-optional)
  - [Usage](#usage)
  - [How to](#how-to)
    - [How to Notify superuser when connected with another user](#how-to-notify-superuser-when-connected-with-another-user)
    - [How to use django-su with a custom user model (AUTH\_USER\_MODEL)](#how-to-use-django-su-with-a-custom-user-model-auth_user_model)
  - [Testing & Quality](#testing--quality)
    - [Unit Testing](#unit-testing)
    - [Linting & Formatting](#linting--formatting)
  - [Project Layout](#project-layout)
  - [License](#license)
  - [Credits](#credits)

About
-----------------

**django-su** is a Django package that allows a superuser to log in as any other user from the Django admin interface, then switch back to their original session when done.

- **Minimal footprint**: integrates with the standard Django admin without requiring a separate UI framework.
- **Safe session handling**: preserves the original superuser session and prevents `last_login` from being updated on impersonation.
- **Configurable**: redirect URLs, login permission callbacks, and login actions are all overridable via settings.

What's New
-----------------

### Version 1.0.0 (Latest)

### Python Packaging Migration

- `pyproject.toml`: The package now uses PEP 517/518 (`pyproject.toml` + `setuptools`) instead of `setup.py`. Version is read dynamically from `django_su/VERSION`.

### Extended Django and Python Support

- **Django 4.2, 5.0, 6.0** are now declared in the package classifiers.
- **Python 3.11 / 3.13** compatibility: updated `collections.abc` imports and other stdlib references.
- **Linting**: `ruff` is used for lint and format checks (see `ruff.toml`).

Installation
-----------------

1. Either checkout `django_su` from GitHub, or install using `pip`:

    ```bash
    pip install django-su
    ```

1. Add `django_su` to your `INSTALLED_APPS`. Make sure you put it *before* `django.contrib.admin`:

    ```python
    INSTALLED_APPS = (
        ...
        'django_su',  # must be before ``django.contrib.admin``
        'django.contrib.admin',
    )
    ```

1. Add `SuBackend` to `AUTHENTICATION_BACKENDS`:

    ```python
    AUTHENTICATION_BACKENDS = (
        ...
        'django_su.backends.SuBackend',
    )
    ```

1. Update your `urls.py` file:

    ```python
    urlpatterns = [
        path('su/', include('django_su.urls')),
        ...
    ]
    ```

And that should be it!

`django-su` requires Django 3.2 or above.

### External dependencies (optional, but recommended)

The following apps are optional but will enhance the user experience:

- The login su form will render using [django-form-admin](https://github.com/darklow/django-form-admin)
- The user selection widget will render using [django-ajax-selects](https://github.com/crucialfelix/django-ajax-selects)

Note that [django-ajax-selects](https://github.com/crucialfelix/django-ajax-selects) requires the following setting:

```python
AJAX_LOOKUP_CHANNELS = {'django_su': dict(model='auth.user', search_field='username')}
```

Building & Packaging
-----------------

This project uses [PEP 517/518](https://peps.python.org/pep-0518/) with `pyproject.toml`. The recommended build tool is [`build`](https://pypi.org/project/build/).

```bash
# Clean old builds
rm -rf dist build *.egg-info

# Install build tools
python -m pip install --upgrade build setuptools wheel

# Build wheel + source distribution
python -m build

# Inspect the distribution
ls dist/
```

Testing The Build
-----------------

Install into a fresh virtual environment to verify:

```bash
python -m venv .venv-test
source .venv-test/bin/activate

pip install dist/django_su-*.whl

python -c "from importlib.metadata import version; print('Installed version:', version('django_su'))"

deactivate
```

Development Workflow
-----------------

Install all dev dependencies:

```bash
pip install -e ".[dev]"
```

Lint, format, and test:

```bash
# Lint
ruff check .

# Format
ruff format .

# Run tests
pytest
```

Configuration (Optional)
-----------------

There are various optional configuration options you can set in your `settings.py`:

```python
# URL to redirect after the login.
# Default: "/"
SU_LOGIN_REDIRECT_URL = "/"

# URL to redirect after the logout.
# Default: "/"
SU_LOGOUT_REDIRECT_URL = "/"

# A function specifying the permissions a user requires in order
# to use the django-su functionality.
# Default: None
SU_LOGIN_CALLBACK = "example.utils.su_login_callback"

# A function to override the django.contrib.auth.login(request, user)
# view, thereby allowing one to set session data, etc.
# Default: None
SU_CUSTOM_LOGIN_ACTION = "example.utils.custom_login"
```

Usage
-----------------

Go and view a user in the admin interface and look for a new "Login as" button in the top right.

Once you have su'ed into a user, you can exit back to your original user by navigating to `/su/` in your browser.

How to
-----------------

### How to Notify superuser when connected with another user

This option warns the superuser when working as another user. To activate:

1. Add `django_su.context_processors.is_su` to `TEMPLATE_CONTEXT_PROCESSORS`:

    ```python
    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django_su.context_processors.is_su',
    )
    ```

1. In your `base.html` include the `su/is_su.html` snippet:

    ```html+django
    {% include "su/is_su.html" %}
    ```

### How to use django-su with a custom user model (AUTH_USER_MODEL)

Django-su should function normally with a custom user model. However, your `ModelAdmin` in `admin.py` will need tweaking:

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    # The following two lines are needed:
    change_form_template = "admin/auth/user/change_form.html"
    change_list_template = "admin/auth/user/change_list.html"
```

This ensures the Django admin uses the correct template customisations for your custom user model.

Testing & Quality
-----------------

### Unit Testing

All tests live under `django_su/tests/`.

- Run all tests:

  ```bash
  pytest
  ```

- Coverage (95% minimum enforced):

  ```bash
  pytest --cov=django_su --cov-report=term-missing
  ```

### Linting & Formatting

[ruff](https://docs.astral.sh/ruff/) is used for both linting and formatting (see `ruff.toml`):

```bash
ruff check .
ruff format .
```

Project Layout
-----------------

```
.
├── LICENSE
├── CHANGES.md
├── MANIFEST.in
├── README.md
├── pyproject.toml
├── ruff.toml
├── setup.cfg
├── django_su
│   ├── VERSION
│   ├── __init__.py
│   ├── backends.py
│   ├── compat.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── locale/
│   ├── models.py
│   ├── templates/
│   ├── templatetags/
│   │   ├── compat.py
│   │   └── su_tags.py
│   ├── tests/
│   │   ├── test_backends.py
│   │   ├── test_context_processors.py
│   │   ├── test_forms.py
│   │   ├── test_template_tags.py
│   │   ├── test_utils.py
│   │   ├── test_version.py
│   │   └── test_views.py
│   ├── urls.py
│   ├── utils.py
│   ├── version.py
│   └── views.py
└── tests
    ├── test_settings.py
    └── test_urls.py
```

- `django_su/` — package source
- `django_su/version.py` — dynamic version loader (reads `django_su/VERSION`)
- `pyproject.toml` — modern build configuration (replaces `setup.py`)
- `MANIFEST.in` — ensures non-Python files (such as `VERSION`) are included in sdists

License
-----------------

This project is licensed under the terms of the [MIT License](LICENSE).

Credits
-----------------

Originally authored by [Adam Charnock](http://adamcharnock.com/), with contributions from the open-source community. See [CHANGES.md](CHANGES.md) for the full history.

- <http://bitkickers.blogspot.com/2010/06/add-button-to-django-admin-to-login-as.html>
- <http://copiousfreetime.blogspot.com/2006/12/django-su.html>
