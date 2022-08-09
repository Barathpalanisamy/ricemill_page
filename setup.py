from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in retail/__init__.py
from retail import __version__ as version

setup(
	name="retail",
	version=version,
	description="Retail",
	author="barath",
	author_email="retail@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
