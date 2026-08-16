#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""OpusLib Package."""

import setuptools  # type: ignore
import platform
import sys
import os

from setuptools.command.build import build

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


def _get_plat_name():
    for index, arg in enumerate(sys.argv):
        if arg == "--plat-name" and index + 1 < len(sys.argv):
            return sys.argv[index + 1]
        if arg.startswith("--plat-name="):
            return arg.split("=", 1)[1]

    return None

if sys.platform.startswith("win"):
    plat_name = _get_plat_name()
    arch, _ = platform.architecture()

    if plat_name in ("win32", "win-arm32"):
        dll_path = "bin/win32/opus.dll"
    elif plat_name in ("win_amd64", "win-amd64", "win64"):
        dll_path = "bin/win64/opus.dll"
    elif arch == "64bit":
        dll_path = "bin/win64/opus.dll"
    else:
        dll_path = "bin/win32/opus.dll"

    # Check that the binary exists so assembly does not fail silently.
    if not os.path.exists(os.path.join("opuslib", dll_path)):
        sys.stderr.write(f"!!! Warning: expected {dll_path} not found\n")

    package_data["opuslib"] = [dll_path]


if sys.platform.startswith("win"):
    class build_platform_lib(build):
        def finalize_options(self):
            super().finalize_options()

            plat_name = _get_plat_name()
            if plat_name is not None:
                plat_specifier = f".{plat_name}-{sys.implementation.cache_tag}"
                self.build_platlib = os.path.join(
                    self.build_base,
                    "lib" + plat_specifier
                )

            if self.build_lib is None or self.build_lib == self.build_purelib:
                self.build_lib = self.build_platlib

    cmdclass["build"] = build_platform_lib


if sys.platform.startswith("win") and bdist_wheel is not None:
    class bdist_wheel_platform_tag(bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            self.plat_name_supplied = True

            plat_name = _get_plat_name()
            if plat_name is not None:
                self.bdist_dir = os.path.join(
                    "build",
                    "bdist." + plat_name,
                    "wheel"
                )

        def get_tag(self):
            _python, _abi, platform_tag = super().get_tag()
            return "py3", "none", platform_tag

    cmdclass["bdist_wheel"] = bdist_wheel_platform_tag

setuptools.setup(
    name='opuslib',
    version='3.0.5',
    author='Никита Кузнецов',
    author_email='self@svartalf.info',
    maintainer='Orion Labs, Inc.',
    maintainer_email='code@orionlabs.io',
    license='BSD 3-Clause License',
    url='https://github.com/jawhien/opuslib',
    project_urls={
        'Original repository': 'https://github.com/orion-labs/opuslib',
    },
    description='Python bindings to the libopus, IETF low-delay audio codec',
    packages=('opuslib', 'opuslib.api'),
    package_data=package_data,
    cmdclass=cmdclass,
    include_package_data=False,
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
    ],
)
