from setuptools import setup

setup(
    zip_safe=True,
    name='desafe',
    version='0.0.3',
    author='pjon',
    py_modules=['desafe'],
    description='An utility to decrypt Safe in Cloud password files',
    license='LICENSE',
    install_requires=[
        "pycrypto",
        "xmltodict",
        "passlib",
        "docopt"
    ],
    entry_points={
        'console_scripts': [
            'desafe = desafe:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS'
    ]

)
