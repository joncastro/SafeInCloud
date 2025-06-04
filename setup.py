from setuptools import setup

import os
import re

if os.environ.get("CI_COMMIT_TAG"):
    version = os.environ["CI_COMMIT_TAG"]
    if version.startswith("v"):
        version = version[1:]
        if not re.search(r"^\d+\.\d+\.\d+$", version):
            raise AttributeError(
                "given CI_COMMIT_TAG {} incorrect format. It must be vX.Y.Z or X.Y.Z format".format(
                    os.environ["CI_COMMIT_TAG"]
                )
            )
elif os.environ.get("CI_JOB_ID"):
    version = os.environ["CI_JOB_ID"]
else:
    version = None


setup(
    zip_safe=True,
    name="desafe",
    version=version,
    author="pjon",
    url="https://github.com/joncastro/SafeInCloud",
    py_modules=["desafe"],
    description="An utility to decrypt Safe in Cloud password files",
    license="LICENSE",
    install_requires=["pycryptodomex", "xmltodict", "passlib", "docopt"],
    entry_points={"console_scripts": ["desafe = desafe:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
)
