"""
setup.py
"""
from distutils.core import setup

VERSION = "0.9.0"

setup(
    name="django_su",
    version=VERSION,
    description="child of django-su package(django's)",
    author="Django, Updated by Lalithkumar",
    url='https://sendhub.com/',
    packages=['django_su'],
    package_data={'sendhub': [VERSION]}
)
