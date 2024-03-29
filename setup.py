import io
import os
import os.path as op

from setuptools import PEP420PackageFinder  # isort: skip
from distutils.core import setup  # isort: skip


ROOT = op.dirname(op.abspath(__file__))
SRC = op.join(ROOT, "src")
print(ROOT)


def get_install_req():
    with io.open(ROOT + "/deploy/requirements.txt") as fh:
        install_reqs = fh.read()
    install_reqs = [l for l in install_reqs.split("\n") if len(l) > 1]
    return install_reqs


install_reqs = get_install_req()


def get_version_info():
    """Extract version information as a dictionary from version.py."""
    version_info = {}
    version_filename = os.path.join(ROOT, "src", "housepred", "version.py")
    with open(version_filename, "r") as version_module:
        version_code = compile(version_module.read(), "version.py", "exec")
    exec(version_code, version_info)
    return version_info


setup(
    name="housepred",
    version=get_version_info()["version"],
    package_dir={"": "src"},
    description="Predicting House Prices",
    author="Pushvinder Kumar Rohtagi",
    packages=PEP420PackageFinder.find(where=str(SRC)),
    python_requires=">=3.8.1",
    install_requires=install_reqs,
    tests_require=["pytest"],
)
