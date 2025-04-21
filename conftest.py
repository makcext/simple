# flake8: noqa: E501
"""
Pytest global settings
"""

import os

import pytest

# Debugger settings for PyTest
if os.environ.get("PYTEST_DEBUGGER"):
    import debugpy

    debugpy.listen(("0.0.0.0", 3002))

    S_RED = "\033[91m"
    E_RED = "\033[0m"

    print("\n" + S_RED + "Waiting for debugger to be attached on 3002 port" + E_RED)
    debugpy.wait_for_client()
