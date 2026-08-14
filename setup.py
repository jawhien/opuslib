#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""OpusLib Package."""

import setuptools  # type: ignore
import platform
import sys
import os

try:
    from setuptools.command.bdist_wheel import bdist_wheel
except ImportError:
    try:
        from wheel.bdist_wheel import bdist_wheel
    except ImportError:
        bdist_wheel = None

__author__ = 'Никита Кузнецов <self@svartalf.info>'
__copyright__ = 'Copyright (c) 2012, SvartalF'
__license__ = 'BSD 3-Clause License'

cmdclass = {}
package_data = {}

if sys.platform.startswith("win"):
    # Defining the Python architecture (not just the OS)
    arch, _ = platform.architecture()
    if arch == "64bit":
        dll_path = "bin/win64/opus.dll"
    else:
        dll_path = "bin/win32/opus.dll"

    # Let's check that the binary exists (so that the assembly does not fail silently)
    if not os.path.exists(os.path.join("opuslib", dll_path)):
        sys.stderr.write(f"!!! Warning: expected {dll_path} not found\n")

    package_data["opuslib"] = [dll_path]


if sys.platform.startswith("win") and bdist_wheel is not None:
    class bdist_wheel_platform_tag(bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            self.root_is_pure = False

        def get_tag(self):
            _python, _abi, platform_tag = super().get_tag()
            return "py3", "none", platform_tag

    cmdclass["bdist_wheel"] = bdist_wheel_platform_tag

setuptools.setup(
    name='opuslib',
    version='3.0.4',
    author='Никита Кузнецов',
    author_email='self@svartalf.info',
    maintainer='Orion Labs, Inc.',
    maintainer_email='code@orionlabs.io',
    license='BSD 3-Clause License',
    url='https://github.com/jawhien/opuslib',
    description='Python bindings to the libopus, IETF low-delay audio codec',
    packages=('opuslib', 'opuslib.api'),
    package_data=package_data,
    cmdclass=cmdclass,
    include_package_data=False,
    test_suite='tests',
    zip_safe=False,
    tests_require=[
        'coverage >= 4.4.1',
        'nose >= 1.3.7',
    ],
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
    ),
)
