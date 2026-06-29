# Changelog

All notable changes to django-su are documented here.

---

## SendHub Internal Fork — 29 Jun 2026

- Migrate packaging from `setup.py` to `pyproject.toml` (setuptools build backend)
- Add `ruff.toml` for linting; apply ruff-formatted import ordering and double-quote strings project-wide
- Drop dead code paths in `compat.py` for Django < 1.5, < 1.6, and < 1.8; mark remaining legacy branches with `# pragma: no cover`
- Replace old-style `class Foo(object):` with `class Foo:` and `super(ClassName, self)` with `super()` throughout
- Remove `# -*- coding: utf-8 -*-` encoding declarations (implicit in Python 3)
- Reorganise imports alphabetically across all modules
- Disable `@require_http_methods(['POST'])` on `login_as_user` view to support GET-based internal impersonation flows
- Remove unused `user_logged_in` signal import from `views.py`
- Expand `.gitignore` to cover standard Python/Django project artifacts (caches, virtual environments, IDE files)
- Add test suite under `django_su/tests/` and `tests/` with `conftest.py` and `pytest-django` configuration
- Add `VERSION` file and `django_su/version.py` for programmatic version access

---

## Version 1.0.0 — Fri 1 May 2022

- Fix compatibility with Django 4.0
- Test in Django versions 2.2–4.0, Python versions 3.7–3.10

---

## Version 0.9.0 — Mon 20 Jan 2020

- Update `setup.py` for Django version support changes
- Migrate away from `django-setuptest` (no longer maintained)
- Update CI config for Django 3 and Python 3.8
- Remove deprecated template loader `admin_static` in favour of `static`
- Drop support for Django < 1.11
- Call `get_user_model` once per method (minor optimisation)
- Update argument of `django_su.backends.authenticate` function
- Update `UserSuForm` to enhance compatibility with custom user models
- Document use of `AUTH_USER_MODEL` with django-su

---

## Version 0.8.0 — Sat 15 Sep 2018

- Update argument of `django_su.backends.authenticate` function
- Update `UserSuForm` to enhance compatibility with custom user models
- Document use of `AUTH_USER_MODEL` with django-su

---

## Version 0.7.0 — Mon 13 Aug 2018

- Add `request` to the `authenticate` call

---

## Version 0.6.0 — Mon 18 Dec 2017

- Fixes for Django 2.0; update `Signal.disconnect()` usage for `last_login`
- Fix relocation of `django.core.urlresolvers` → `django.urls` (Django 2)
- Drop support for Django 1.4
- Drop Python 2.6 and 3.3 from support matrix
- No need for su when adding a new user
- Upgrade test suite; fix broken exception handler
- Fix `compat.py`, `MANIFEST.in`; add new translation (Gustavo Santana)
- Ensure `compat` template tag library is loaded
- Customise `admin/base_site.html` (fix #54)
- Ensure all CSRF protection is enabled
- Disable CI for Django 2.0 on Python 2.7

---

## Version 0.5.2 — Wed 20 Apr 2016

- Re-enable `formadmin`
- Add `UsersLookup` example
- Make `example` project work with Django 1.9+
- Replace `render_to_response` with `render`

---

## Version 0.5.1 — Wed 23 Mar 2016

- Fix su with `django-suit` (fix #48)
- Use Django's module loading utils (fix #45)
- Fix for Django 1.10
- Various example project updates

---

## Version 0.5.0 — Fri 27 Nov 2015

- Prevent updating a user's `last_login` field when su'ing
- Sort users by username in the basic non-ajax user select (#41)
- Add `context_processor` and a template element
- Add `ru` (Russian) translation

---

## Version 0.4.8 — Fri 03 Jul 2015

- Allow negative user IDs (fix #30)
- Improve Python 3 compatibility
- Restrict login views to POST only to avoid potential CSRF issues

---

## Version 0.4.7 — Wed 09 Jul 2014

- Fix for Django 1.4

---

## Version 0.4.6 — Wed 09 Jul 2014

_(no changes recorded)_

---

## Version 0.4.5 — Sat 24 May 2014

- Add ability to override `auth.login` function
- Add `su_exit` for the `auth.login` override

---

## Version 0.4.4 — Sat 24 May 2014

- Move `django_su` into top-level directory (clean up `src/` usage)

---

## Version 0.4.3 — Sat 24 May 2014

- Fix `login_link` template on Django 1.4

---

## Version 0.4.2 — Fri 03 Jan 2014

- Fix object tools showing only for user pages, not group pages
- Add class for `django-grappelli` support (no-op on vanilla admin)

---

## Version 0.4.1 — Fri 20 Dec 2013

- Fix import error for Django 1.6

---

## Version 0.4.0 — Mon 09 Sep 2013

- Remove deprecated `adminmedia` usage

---

## Version 0.3.2 — Wed 21 Aug 2013

- Minor README updates

---

## Version 0.3.1 — Tue 20 Aug 2013

- Add `long_description` to `setup.py`
- Update README

---

## Version 0.3.0 — Tue 20 Aug 2013

- Add MIT licence (fix #8)
- Update `setup.py`
- Update URL calls for Django 1.5 compatibility
- Better handling of auth backend
- Django 1.4 `get_user_model` fix
- Modify deprecated template tags for Django 1.5 compatibility
- `SU_LOGIN` can now be either a string or a callable
- Add a logout view
