#!/usr/bin/env python3
"""
upppdf - Unlock Password Protected PDF

A Python package for unlocking password-protected PDF files using multiple methods
including brute force attacks, known password lists, and various PDF libraries.
"""

from .version import __version__, __version_info__
from .pdf_unlocker import PDFUnlocker, PasswordMemory, main

__all__ = ["PDFUnlocker", "PasswordMemory", "main", "__version__", "__version_info__"]