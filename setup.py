from setuptools import (
    setup,
    find_packages,
)

import mpc

setup(
    name='PyDecentralizedMPC',
    version='0.0.1',
    license='MIT',
    py_modules=['mpc'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'utilitybelt'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
    ]
)