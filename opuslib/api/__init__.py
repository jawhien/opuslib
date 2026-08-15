#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
#

"""OpusLib Package."""

import ctypes  # type: ignore
from ctypes.util import find_library  # type: ignore
import os
import sys
import platform

__author__ = 'Никита Кузнецов <self@svartalf.info>'
__copyright__ = 'Copyright (c) 2012, SvartalF'
__license__ = 'BSD 3-Clause License'


class OpusLibraryError(RuntimeError):
    """Raised when libopus cannot be loaded."""


_pkg_dir = os.path.dirname(os.path.dirname(__file__))

lib_location = None

if sys.platform.startswith("win"):

    arch, _ = platform.architecture()
    if arch == "64bit":
        dll_path = os.path.join(_pkg_dir, "bin", "win64", "opus.dll")
    else:
        dll_path = os.path.join(_pkg_dir, "bin", "win32", "opus.dll")

    if os.path.exists(dll_path):
        lib_location = dll_path
    else:
        raise OpusLibraryError(
            f"Could not find bundled Opus library at {dll_path}"
        )
else:
    lib_location = find_library("opus")
    if lib_location is None:
        raise OpusLibraryError(
            "Could not find system Opus library. Make sure it is installed."
        )

libopus = ctypes.CDLL(lib_location)

c_int_pointer = ctypes.POINTER(ctypes.c_int)
c_int16_pointer = ctypes.POINTER(ctypes.c_int16)
c_float_pointer = ctypes.POINTER(ctypes.c_float)
